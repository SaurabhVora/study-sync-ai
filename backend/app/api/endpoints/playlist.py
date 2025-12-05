from typing import List
from fastapi import APIRouter, HTTPException
from app.models.playlist import PlaylistGenerateRequest, PlaylistResponse, VideoResult
from app.services.youtube import youtube_service
from app.services.ai_sentiment import sentiment_service
from app.services.gap_filler import gap_filler_service

router = APIRouter()

@router.post("/generate", response_model=PlaylistResponse)
async def generate_playlist(request: PlaylistGenerateRequest):
    """
    Generates a playlist for a given topic by searching YouTube.
    Uses AI Sentiment Analysis to rank videos.
    Uses AI Gap Filling to suggest missing prerequisites.
    """
    print(f"🔍 Generating playlist for: {request.topic_name}")
    
    # 1. Search YouTube
    videos_data = youtube_service.search_videos(request.topic_name, max_results=request.limit)
    
    if not videos_data:
        raise HTTPException(status_code=404, detail="No videos found for this topic")

    # 2. Analyze Videos (Fetch Comments + AI Score)
    print(f"🧠 Analyzing {len(videos_data)} videos with AI...")
    
    results = []
    current_video_titles = []
    
    for v in videos_data:
        video_id = v["video_id"]
        current_video_titles.append(v["title"])
        
        # Fetch Comments
        comments = youtube_service.get_video_comments(video_id)
        
        # AI Sentiment Analysis
        if comments:
            score = sentiment_service.analyze_comments(comments)
        else:
            score = 50.0 
            
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

    # 3. Rank by AI Score
    results.sort(key=lambda x: x.ai_score, reverse=True)

    # 4. Gap Filling (Experimental)
    # Check if this topic belongs to a known subject (e.g., "Operating Systems")
    # For now, we assume "Operating Systems" context if the user searches for OS topics
    # In a full app, we would know the Subject context from the UI
    gaps = gap_filler_service.find_gaps("Operating Systems", current_video_titles)
    
    # If gaps found, we could fetch videos for them too (future step)
    # For now, we just log them or could return them in the response
    if gaps:
        print(f"🧩 Suggested Gaps to Fill: {gaps}")

    return PlaylistResponse(topic=request.topic_name, videos=results, gaps=gaps)

# --- Save & Manage Playlists ---

from app.core.supabase import supabase
from app.models.playlist import SavePlaylistRequest, SavedPlaylist

@router.post("/save")
async def save_playlist(request: SavePlaylistRequest):
    """Saves a generated playlist to the user's library."""
    print(f"💾 Saving playlist '{request.topic_name}' for user {request.user_id}")
    
    # 1. Insert into 'playlists' table
    playlist_data = {
        "user_id": request.user_id,
        "name": request.topic_name,
        "description": f"AI Generated playlist for {request.topic_name}"
    }
    print(f"Payload: {playlist_data}")

    try:
        res = supabase.table("playlists").insert(playlist_data).execute()
        print(f"Insert Result: {res}")
    except Exception as e:
        print(f"Error inserting playlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to save playlist")
        
    playlist_id = res.data[0]["id"]
    
    # 2. Insert videos into 'playlist_items'
    items_data = []
    for i, video in enumerate(request.videos):
        items_data.append({
            "playlist_id": playlist_id,
            "resource_id": None, # We aren't linking to 'resources' table yet for simplicity
            "video_id": video.video_id, # Storing raw video_id for now
            "title": video.title,
            "url": f"https://www.youtube.com/watch?v={video.video_id}",
            "position": i
        })
        
    if items_data:
        supabase.table("playlist_items").insert(items_data).execute()
        
    return {"status": "success", "playlist_id": playlist_id}

@router.get("/user/{user_id}", response_model=List[SavedPlaylist])
async def get_user_playlists(user_id: str):
    """Fetches all saved playlists for a user."""
    res = supabase.table("playlists").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
    return res.data

@router.delete("/{playlist_id}")
async def delete_playlist(playlist_id: str):
    """Deletes a playlist."""
    print(f"🗑️ Deleting playlist: {playlist_id}")
    # Cascade delete should handle items if configured, but let's be safe
    try:
        supabase.table("playlist_items").delete().eq("playlist_id", playlist_id).execute()
        supabase.table("playlists").delete().eq("id", playlist_id).execute()
    except Exception as e:
        print(f"Error deleting playlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"status": "deleted"}
