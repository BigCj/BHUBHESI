import uuid
import datetime
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
import json

from backend.app.config import CLIPS_DIR, STORAGE_DIR, CLEANUP_HOURS, RAW_DIR, AUDIO_DIR
from backend.app.database import engine, Base, get_db, SessionLocal
from backend.app.models import Job, Moment, Clip
from backend.app.schemas import JobCreate, JobResponse, JobDetailResponse
from backend.app.utils.yt_dlp_helper import get_video_metadata
from backend.app.utils.audio_analysis import analyze_audio_features
from backend.app.utils.detection_engine import recalibrate_viral_moments_with_feedback
from backend.app.utils.ffmpeg_helper import extract_clip
from backend.app.worker import add_job_to_queue

# Initialize Database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI App
app = FastAPI(
    title="Viral Moment Extractor API",
    description="Backend API for downloading, transcribing, analyzing and extracting viral clips.",
    version="1.1.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Clip static files folder for direct downloading
app.mount("/api/clips", StaticFiles(directory=str(CLIPS_DIR)), name="clips")

# --- Periodic Cleanup Background Task ---
def cleanup_old_jobs():
    db = SessionLocal()
    try:
        cutoff = datetime.datetime.utcnow() - datetime.timedelta(hours=CLEANUP_HOURS)
        old_jobs = db.query(Job).filter(Job.created_at < cutoff).all()
        
        if not old_jobs:
            return
            
        print(f"[CLEANUP] Found {len(old_jobs)} jobs older than {CLEANUP_HOURS} hours. Starting deletion.")
        
        for job in old_jobs:
            for clip in job.clips:
                clip_path = Path(clip.file_path)
                if clip_path.exists():
                    try:
                        clip_path.unlink()
                    except Exception:
                        pass

            audio_path = STORAGE_DIR / "audio" / f"{job.id}.wav"
            if audio_path.exists():
                try:
                    audio_path.unlink()
                except Exception:
                    pass

            transcript_path = STORAGE_DIR / "transcripts" / f"{job.id}.json"
            if transcript_path.exists():
                try:
                    transcript_path.unlink()
                except Exception:
                    pass

            db.delete(job)
            
        db.commit()
    except Exception as e:
        print(f"[CLEANUP] Error during cleanup: {str(e)}")
    finally:
        db.close()

# Trigger cleanup on startup
@app.on_event("startup")
def startup_event():
    cleanup_old_jobs()

# --- API Routes ---

@app.get("/api/jobs", response_model=List[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    """
    Lists all jobs in reverse chronological order.
    """
    return db.query(Job).order_by(Job.created_at.desc()).all()


@app.post("/api/jobs", response_model=JobResponse, status_code=201)
def create_job(payload: JobCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Receives a YouTube URL, target niche and target clip count,
    initializes the job, and queues it.
    """
    url = payload.youtube_url.strip()
    niche = payload.niche.strip().lower()
    clip_count = payload.clip_count
    
    if not ("youtube.com" in url or "youtu.be" in url):
        raise HTTPException(
            status_code=400, 
            detail="Invalid video URL. Only YouTube links are supported."
        )

    if niche not in ["podcast", "streamer", "sports"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid niche selected. Use 'podcast', 'streamer', or 'sports'."
        )

    try:
        metadata = get_video_metadata(url)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid YouTube URL or unreachable video: {str(e)}"
        )

    video_id = metadata.get('id', 'video')
    job_id = f"{video_id}_{uuid.uuid4().hex[:6]}"

    db_job = Job(
        id=job_id,
        youtube_url=url,
        status="PENDING",
        progress=0,
        niche=niche,
        clip_count=clip_count,
        title=metadata.get('title'),
        duration=metadata.get('duration'),
        thumbnail_url=metadata.get('thumbnail_url')
    )
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    add_job_to_queue(job_id, url)
    background_tasks.add_task(cleanup_old_jobs)

    return db_job


@app.get("/api/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: str, db: Session = Depends(get_db)):
    """
    Retrieves the current status of a job.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/api/jobs/{job_id}/results", response_model=JobDetailResponse)
def get_job_results(job_id: str, db: Session = Depends(get_db)):
    """
    Retrieves the fully processed job results including timeline moments.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status == "FAILED":
        raise HTTPException(
            status_code=400,
            detail=f"Job processing failed: {job.error_message}"
        )
        
    return job


@app.post("/api/moments/{moment_id}/like")
def toggle_like_moment(moment_id: int, db: Session = Depends(get_db)):
    """
    Toggles the liked status of a specific moment clip (User Active Feedback).
    """
    moment = db.query(Moment).filter(Moment.id == moment_id).first()
    if not moment:
        raise HTTPException(status_code=404, detail="Moment not found")
    
    moment.liked = not moment.liked
    db.commit()
    db.refresh(moment)
    
    return {"id": moment.id, "liked": moment.liked}


@app.post("/api/jobs/{job_id}/recalibrate", response_model=JobDetailResponse)
def recalibrate_job(job_id: str, db: Session = Depends(get_db)):
    """
    Active Learning Feedback endpoint.
    Retrieves user liked templates, recalculates virality matches, precision cuts
    new clips on-the-fly, and appends them immediately to the workspace.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status != "COMPLETED":
        raise HTTPException(
            status_code=400,
            detail="Cannot recalibrate a job that is not completed."
        )

    # 1. Fetch liked moments
    liked_moments_db = db.query(Moment).filter(Moment.job_id == job_id, Moment.liked == True).all()
    if not liked_moments_db:
        raise HTTPException(
            status_code=400,
            detail="Please star/like at least one moment clip in the workspace before recalibrating."
        )

    # Convert liked moments database objects to list of dictionaries
    liked_moments = []
    for lm in liked_moments_db:
        liked_moments.append({
            'start_time': lm.start_time,
            'end_time': lm.end_time,
            'loudness_score': lm.loudness_score,
            'contrast_score': lm.contrast_score,
            'frequency_score': lm.frequency_score,
            'speech_rate_score': lm.speech_rate_score,
            'keyword_score': lm.keyword_score
        })

    try:
        # 2. Load cached transcripts and analyze audio WAV file
        transcript_path = STORAGE_DIR / "transcripts" / f"{job_id}.json"
        audio_path = STORAGE_DIR / "audio" / f"{job_id}.wav"
        
        # Verify files are present
        if not transcript_path.exists() or not audio_path.exists():
            raise FileNotFoundError("Cached transcript or audio analysis files have expired or are missing.")

        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_data = json.load(f)

        audio_features = analyze_audio_features(audio_path)

        # 3. Run Active Learning feedback vector similarity logic
        new_moments = recalibrate_viral_moments_with_feedback(
            audio_features=audio_features,
            transcript_features=transcript_data,
            liked_moments=liked_moments,
            clip_count=job.clip_count
        )

        # 4. If we need the raw video file to perform precision cuts, download it temporarily
        # We delete it immediately afterward to maintain clean local storage
        video_path = RAW_DIR / f"{job_id}.mp4"
        raw_downloaded = False
        
        if not video_path.exists():
            # Temporarily download for clipping
            from backend.app.utils.yt_dlp_helper import download_video_and_audio
            # Download again (will reuse yt-dlp cache / fast best format merge)
            # Since we only extract a few 15s clips, download is extremely fast
            # We don't overwrite audio_path, we just need the video
            temp_video_path, _ = download_video_and_audio(job.youtube_url, job_id)
            raw_downloaded = True

        # Write new moments and extract new clips
        db_moments = []
        for m in new_moments:
            # Check if an identical moment already exists in the database
            exists = db.query(Moment).filter(
                Moment.job_id == job_id,
                Moment.start_time == m['start_time'],
                Moment.end_time == m['end_time']
            ).first()
            
            if exists:
                continue

            db_moment = Moment(
                job_id=job_id,
                start_time=m['start_time'],
                end_time=m['end_time'],
                viral_score=m['viral_score'],
                reason=m['reason'],
                liked=False,
                loudness_score=m['loudness_score'],
                contrast_score=m['contrast_score'],
                frequency_score=m['frequency_score'],
                speech_rate_score=m['speech_rate_score'],
                keyword_score=m['keyword_score'],
                hook_score=m['hook_score'],
                tension_score=m['tension_score'],
                payoff_score=m['payoff_score'],
                resolution_score=m['resolution_score']
            )
            db.add(db_moment)
            db_moments.append(db_moment)

        db.commit() # Save moments to obtain IDs

        # Extract FFmpeg raw clips
        for db_moment in db_moments:
            clip_filename = f"{job_id}_{db_moment.id}.mp4"
            
            clip_path = extract_clip(
                video_path=video_path,
                start_time=db_moment.start_time,
                end_time=db_moment.end_time,
                output_filename=clip_filename
            )

            file_size = clip_path.stat().st_size
            download_url = f"/api/clips/{clip_filename}"

            db_clip = Clip(
                job_id=job_id,
                moment_id=db_moment.id,
                filename=clip_filename,
                file_path=str(clip_path),
                file_size=file_size,
                download_url=download_url
            )
            db.add(db_clip)

        db.commit()

        # Clean up temporary raw video file
        if raw_downloaded and video_path.exists():
            video_path.unlink()

        db.refresh(job)
        return job

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Recalibration failed during audio/clip slice operations: {str(e)}"
        )
