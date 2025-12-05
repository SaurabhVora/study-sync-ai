from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PlaylistGenerateRequest(BaseModel):
    topic_name: str
    limit: int = 5

class VideoResult(BaseModel):
    video_id: str
    title: str
    description: str
    thumbnail: str
    channel_title: str
    publish_time: str
    ai_score: Optional[float] = None
    
class PlaylistResponse(BaseModel):
    topic: str
    videos: List[VideoResult]
    gaps: Optional[List[str]] = []

# --- New Models for Saving ---

class SavePlaylistRequest(BaseModel):
    user_id: str
    topic_name: str
    videos: List[VideoResult]

class SavedPlaylist(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
