from pydantic import BaseModel
from typing import List, Optional

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
