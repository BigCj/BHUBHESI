import subprocess
import os
from pathlib import Path
from backend.app.config import FFMPEG_PATH, CLIPS_DIR

def extract_clip(video_path: Path, start_time: float, end_time: float, output_filename: str) -> Path:
    """
    Precision cuts the video file from start_time to end_time.
    Uses visually lossless broadcast-quality encoding (-crf 18) and high quality AAC audio.
    """
    output_path = CLIPS_DIR / output_filename
    
    if not video_path.exists():
        raise FileNotFoundError(f"Source video not found at {video_path}")

    if output_path.exists():
        output_path.unlink()

    duration = end_time - start_time
    
    # CRF 18 is recognized as visually lossless in the x264 codec
    cmd = [
        FFMPEG_PATH,
        '-y',
        '-ss', f"{start_time:.3f}",
        '-i', str(video_path),
        '-t', f"{duration:.3f}",
        '-c:v', 'libx264',
        '-preset', 'superfast',
        '-crf', '18',
        '-c:a', 'aac',
        '-b:a', '192k',  # higher audio bitrate for clean sound
        '-strict', '-2',
        str(output_path)
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode('utf-8', errors='ignore') if e.stderr else ""
        raise RuntimeError(f"FFmpeg clipping failed for {output_filename}: {stderr}")

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise RuntimeError(f"FFmpeg completed but clip file was not created or is empty: {output_filename}")

    return output_path
