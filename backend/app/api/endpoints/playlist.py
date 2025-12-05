from fastapi import APIRouter, HTTPException
from app.models.playlist import PlaylistGenerateRequest, PlaylistResponse, VideoResult
from app.services.youtube import youtube_service
from app.services.ai_sentiment import sentiment_service
import asyncio

router = APIRouter()

@router.post("/generate", response_model=PlaylistResponse)
async def generate_playlist(request: PlaylistGenerateRequest):
    """
    Generates a playlist for a given topic by searching YouTube.
    Uses AI Sentiment Analysis to rank videos based on comment quality.
    """
    print(f"🔍 Generating playlist for: {request.topic_name}")
    
    # 1. Search YouTube
    videos_data = youtube_service.search_videos(request.topic_name, max_results=request.limit)
    
    if not videos_data:
        raise HTTPException(status_code=404, detail="No videos found for this topic")

    # 2. Analyze Videos (Fetch Comments + AI Score)
    print(f"🧠 Analyzing {len(videos_data)} videos with AI...")
    
    results = []
    
    # We process videos sequentially for now to avoid hitting YouTube API rate limits too hard
    # In production, this should be parallelized with asyncio.gather
    for v in videos_data:
        video_id = v["video_id"]
        
        # Fetch Comments
        comments = youtube_service.get_video_comments(video_id)
        
        # AI Sentiment Analysis
        if comments:
            score = sentiment_service.analyze_comments(comments)
        else:
            score = 50.0 # Neutral score if disabled comments
            
        print(f"   - Video: {v['title'][:30]}... | Score: {score}")
        
        results.append(VideoResult(
            video_id=video_id,
            title=v["title"],
            description=v["description"],
            thumbnail=v["thumbnail"],
            channel_title=v["channel_title"],
            publish_time=v["publish_time"],
            ai_score=score
        ))

    # 3. Rank by AI Score (Highest First)
    results.sort(key=lambda x: x.ai_score, reverse=True)

    return PlaylistResponse(topic=request.topic_name, videos=results)
