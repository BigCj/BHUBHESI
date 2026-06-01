import subprocess
import yt_dlp
import os
from pathlib import Path
from backend.app.config import RAW_DIR, AUDIO_DIR, FFMPEG_PATH

def get_video_metadata(url: str) -> dict:
    """
    Extracts video metadata (title, duration, thumbnail, id) without downloading.
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            # Find a suitable thumbnail
            thumbnail = info.get('thumbnail')
            if 'thumbnails' in info and info['thumbnails']:
                thumbnail = info['thumbnails'][-1].get('url')
            
            return {
                'id': info.get('id'),
                'title': info.get('title'),
                'duration': float(info.get('duration', 0)),
                'thumbnail_url': thumbnail,
            }
        except Exception as e:
            raise RuntimeError(f"Failed to fetch metadata from {url}: {str(e)}")

def download_video_and_audio(url: str, job_id: str, progress_callback=None) -> tuple[Path, Path]:
    """
    Downloads YouTube video at absolute highest available resolution and extracts mono 16kHz WAV audio.
    Returns: (video_path, audio_path)
    """
    video_path = RAW_DIR / f"{job_id}.mp4"
    audio_path = AUDIO_DIR / f"{job_id}.wav"

    class YTDLProgressLogger:
        def __init__(self, cb):
            self.cb = cb
            
        def debug(self, msg):
            if self.cb and '[download]' in msg and '%' in msg:
                try:
                    parts = msg.split()
                    for p in parts:
                        if '%' in p:
                            pct = float(p.replace('%', ''))
                            overall_pct = int(pct * 0.4)
                            self.cb(overall_pct)
                            break
                except Exception:
                    pass

        def info(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            pass

    # Fetch absolute best video quality + best audio, merging into MP4 container
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': str(video_path).replace('.mp4', ''),
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
        'logger': YTDLProgressLogger(progress_callback),
    }

    if video_path.exists():
        video_path.unlink()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            raise RuntimeError(f"Video download failed: {str(e)}")

    if not video_path.exists():
        files = list(RAW_DIR.glob(f"{job_id}.*"))
        if files:
            files[0].rename(video_path)
        else:
            raise FileNotFoundError(f"yt-dlp finished but no video file was found for job {job_id}")

    # Extract Audio separately using FFmpeg
    if audio_path.exists():
        audio_path.unlink()

    cmd = [
        FFMPEG_PATH,
        '-y',
        '-i', str(video_path),
        '-vn',
        '-ac', '1',
        '-ar', '16000',
        '-acodec', 'pcm_s16le',
        str(audio_path)
    ]

    try:
        if progress_callback:
            progress_callback(42)
        
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if progress_callback:
            progress_callback(45)
            
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode('utf-8', errors='ignore') if e.stderr else ""
        raise RuntimeError(f"Audio extraction failed: {stderr}")

    return video_path, audio_path
