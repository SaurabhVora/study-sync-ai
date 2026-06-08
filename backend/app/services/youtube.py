import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

class YouTubeService:
    def __init__(self):
        if not YOUTUBE_API_KEY:
            print("Warning: YOUTUBE_API_KEY is not set. Scraper will fail.")

    def search_videos(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Searches for videos on YouTube matching the query.
        """
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "key": YOUTUBE_API_KEY
        }
        
        response = requests.get(YOUTUBE_SEARCH_URL, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching from YouTube: {response.text}")
            return []
            
        data = response.json()
        videos = []
        
        for item in data.get("items", []):
            # Safe-guard to only process actual videos
            item_id = item.get("id")
            if not isinstance(item_id, dict) or "videoId" not in item_id:
                continue
                
            video_id = item_id["videoId"]
            snippet = item.get("snippet", {})
            
            # Safe-guard for thumbnails
            thumbnails = snippet.get("thumbnails", {})
            thumbnail_url = ""
            if "high" in thumbnails and isinstance(thumbnails["high"], dict):
                thumbnail_url = thumbnails["high"].get("url", "")
            elif "default" in thumbnails and isinstance(thumbnails["default"], dict):
                thumbnail_url = thumbnails["default"].get("url", "")
            
            videos.append({
                "video_id": video_id,
                "title": snippet.get("title", "No Title"),
                "description": snippet.get("description", ""),
                "thumbnail": thumbnail_url,
                "channel_title": snippet.get("channelTitle", "Unknown Channel"),
                "publish_time": snippet.get("publishTime", "")
            })
            
        return videos


    def get_video_comments(self, video_id: str, max_comments: int = 20) -> List[str]:
        """
        Fetches top comments for a specific video.
        """
        url = "https://www.googleapis.com/youtube/v3/commentThreads"
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": max_comments,
            "order": "relevance", # Get top rated comments
            "key": YOUTUBE_API_KEY
        }
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            # Comments might be disabled
            return []
            
        comments = []
        data = response.json()
        for item in data.get("items", []):
            text = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            comments.append(text)
            
        return comments

# Singleton instance
youtube_service = YouTubeService()
