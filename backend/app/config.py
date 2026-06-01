import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"

# Sub-storage dirs
RAW_DIR = STORAGE_DIR / "raw"
AUDIO_DIR = STORAGE_DIR / "audio"
CLIPS_DIR = STORAGE_DIR / "clips"
TRANSCRIPTS_DIR = STORAGE_DIR / "transcripts"

# Create all folders
for folder in [RAW_DIR, AUDIO_DIR, CLIPS_DIR, TRANSCRIPTS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Database
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{STORAGE_DIR}/database.db")

# Whisper Speech-to-Text Settings
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "tiny")  # Options: tiny, base, small, medium, large
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")  # cpu, mps, cuda

# Clipper Safety Buffers (seconds)
CLIP_BUFFER_PRE = int(os.getenv("CLIP_BUFFER_PRE", "5"))
CLIP_BUFFER_POST = int(os.getenv("CLIP_BUFFER_POST", "5"))

# Clip Auto-delete retention
CLEANUP_HOURS = int(os.getenv("CLEANUP_HOURS", "24"))

# FFmpeg Executable Location
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "ffmpeg")
