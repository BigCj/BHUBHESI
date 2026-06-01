from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# Job Schemas
class JobCreate(BaseModel):
    youtube_url: str = Field(..., description="The YouTube video URL to analyze")
    niche: str = Field("podcast", description="The video niche style (podcast, streamer, sports)")
    clip_count: int = Field(5, description="The target number of highlight clips to generate", ge=1, le=25)

class ClipResponse(BaseModel):
    id: int
    filename: str
    file_size: int
    download_url: str
    created_at: datetime

    class Config:
        from_attributes = True

class MomentResponse(BaseModel):
    id: int
    start_time: float
    end_time: float
    viral_score: float
    reason: str
    liked: bool
    loudness_score: float
    contrast_score: float
    frequency_score: float
    speech_rate_score: float
    keyword_score: float
    
    # Emotional Arc breakdowns
    hook_score: float
    tension_score: float
    payoff_score: float
    resolution_score: float
    
    created_at: datetime
    clip: Optional[ClipResponse] = None

    class Config:
        from_attributes = True

class JobResponse(BaseModel):
    id: str
    youtube_url: str
    status: str
    progress: int
    niche: str
    clip_count: int
    error_message: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[float] = None
    thumbnail_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class JobDetailResponse(JobResponse):
    moments: List[MomentResponse] = []

    class Config:
        from_attributes = True
