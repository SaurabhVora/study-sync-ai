export interface VideoResult {
  video_id: string;
  title: string;
  description: string;
  thumbnail: string;
  channel_title: string;
  publish_time: string;
  ai_score?: number;
}

export interface PlaylistResponse {
  topic: string;
  videos: VideoResult[];
  gaps?: string[];
}
