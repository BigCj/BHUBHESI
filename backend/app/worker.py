import queue
import threading
import traceback
import os
from pathlib import Path
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models import Job, Moment, Clip
from backend.app.utils.yt_dlp_helper import download_video_and_audio
from backend.app.utils.whisper_helper import transcribe_and_analyze_audio
from backend.app.utils.audio_analysis import analyze_audio_features
from backend.app.utils.detection_engine import detect_viral_moments
from backend.app.utils.ffmpeg_helper import extract_clip

# Thread-safe job queue
job_queue = queue.Queue()

def update_job_progress(db: Session, job_id: str, status: str, progress: int, error_message: str = None):
    """
    Safely updates the status, progress, and error message of a job in the database.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.status = status
        job.progress = progress
        if error_message:
            job.error_message = error_message
        db.commit()

def process_job(job_id: str, youtube_url: str):
    """
    Runs the full analysis and clip extraction pipeline.
    """
    db = SessionLocal()
    try:
        # Fetch Job settings (niche and clip_count)
        db_job = db.query(Job).filter(Job.id == job_id).first()
        if not db_job:
            raise ValueError(f"Job {job_id} not found in database on thread start")

        niche = db_job.niche
        clip_count = db_job.clip_count

        # 1. Update status to DOWNLOADING
        update_job_progress(db, job_id, "DOWNLOADING", 5)

        def dl_progress(pct):
            update_job_progress(db, job_id, "DOWNLOADING", pct)

        video_path, audio_path = download_video_and_audio(
            youtube_url, 
            job_id, 
            progress_callback=dl_progress
        )

        # 2. Update status to TRANSCRIBING (45% to 80%)
        update_job_progress(db, job_id, "TRANSCRIBING", 45)

        def transcription_progress(pct):
            update_job_progress(db, job_id, "TRANSCRIBING", pct)

        transcript_data = transcribe_and_analyze_audio(
            audio_path, 
            job_id, 
            progress_callback=transcription_progress
        )

        # 3. Update status to ANALYZING (80% to 90%)
        update_job_progress(db, job_id, "ANALYZING", 80)
        
        audio_features = analyze_audio_features(audio_path)
        
        update_job_progress(db, job_id, "ANALYZING", 85)

        # Run advanced multi-niche emotional arc virality engine
        moments = detect_viral_moments(
            audio_features=audio_features,
            transcript_features=transcript_data,
            niche=niche,
            clip_count=clip_count
        )
        
        # Write moments to DB
        db_moments = []
        for m in moments:
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
        
        db.commit() # Save moments to get autoincremented IDs
        
        # 4. Update status to CLIPPING (90% to 100%)
        update_job_progress(db, job_id, "CLIPPING", 90)

        # Extract FFmpeg clips for each moment
        for i, db_moment in enumerate(db_moments):
            clip_progress = int(90 + (i / len(db_moments)) * 9)
            update_job_progress(db, job_id, "CLIPPING", clip_progress)

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

        # Clean up the massive original raw video file to save disk space
        if video_path.exists():
            video_path.unlink()

        # Complete Job
        update_job_progress(db, job_id, "COMPLETED", 100)

    except Exception as e:
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        update_job_progress(db, job_id, "FAILED", 100, error_message=str(e))
    finally:
        db.close()

def worker_loop():
    while True:
        try:
            job_id, youtube_url = job_queue.get()
            print(f"[WORKER] Starting job {job_id} for URL {youtube_url}")
            process_job(job_id, youtube_url)
            print(f"[WORKER] Finished job {job_id}")
            job_queue.task_done()
        except Exception as e:
            print(f"[WORKER] Error in main worker loop: {str(e)}")

# Start background queue processor
worker_thread = threading.Thread(target=worker_loop, daemon=True)
worker_thread.start()

def add_job_to_queue(job_id: str, youtube_url: str):
    job_queue.put((job_id, youtube_url))
