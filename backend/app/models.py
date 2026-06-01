from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    youtube_url = Column(String, nullable=False)
    status = Column(String, default="PENDING", nullable=False)  # PENDING, DOWNLOADING, TRANSCRIBING, ANALYZING, CLIPPING, COMPLETED, FAILED
    progress = Column(Integer, default=0, nullable=False)  # 0 to 100
    error_message = Column(Text, nullable=True)
    title = Column(String, nullable=True)
    duration = Column(Float, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    niche = Column(String, default="podcast", nullable=False)  # podcast, streamer, sports
    clip_count = Column(Integer, default=5, nullable=False)  # target highlights count
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    moments = relationship("Moment", back_populates="job", cascade="all, delete-orphan")
    clips = relationship("Clip", back_populates="job", cascade="all, delete-orphan")


class Moment(Base):
    __tablename__ = "moments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(Float, nullable=False)  # start of clip in seconds
    end_time = Column(Float, nullable=False)    # end of clip in seconds
    viral_score = Column(Float, nullable=False) # 0 to 100
    reason = Column(Text, nullable=False)       # Description of why it is viral
    liked = Column(Boolean, default=False, nullable=False) # user active feedback

    # Score breakdowns
    loudness_score = Column(Float, default=0.0)
    contrast_score = Column(Float, default=0.0)
    frequency_score = Column(Float, default=0.0)
    speech_rate_score = Column(Float, default=0.0)
    keyword_score = Column(Float, default=0.0)
    
    # Emotional Arc breakdowns (Short form optimized)
    hook_score = Column(Float, default=0.0)
    tension_score = Column(Float, default=0.0)
    payoff_score = Column(Float, default=0.0)
    resolution_score = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    job = relationship("Job", back_populates="moments")
    clip = relationship("Clip", back_populates="moment", uselist=False, cascade="all, delete-orphan")


class Clip(Base):
    __tablename__ = "clips"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    moment_id = Column(Integer, ForeignKey("moments.id", ondelete="CASCADE"), unique=True, nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    download_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    job = relationship("Job", back_populates="clips")
    moment = relationship("Moment", back_populates="clip")
