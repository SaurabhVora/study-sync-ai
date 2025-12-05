"use client";

import { VideoResult } from "@/lib/types";
import { Play, Star, ExternalLink } from "lucide-react";

interface PlaylistViewProps {
  topic: string;
  videos: VideoResult[];
  isLoading: boolean;
}

export function PlaylistView({ topic, videos, isLoading }: PlaylistViewProps) {
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-gray-400 animate-pulse">
        <div className="w-12 h-12 bg-gray-700 rounded-full mb-4"></div>
        <p>AI is analyzing {topic}...</p>
      </div>
    );
  }

  if (!videos.length) {
    return (
      <div className="text-center text-gray-500 mt-20">
        Select a topic to generate a playlist.
      </div>
    );
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6 text-white flex items-center gap-2">
        <Play className="w-6 h-6 text-green-500 fill-green-500" />
        Playlist: {topic}
      </h2>

      <div className="grid gap-4">
        {videos.map((video, index) => (
          <div 
            key={video.video_id}
            className="flex gap-4 p-4 bg-gray-900/50 border border-gray-800 rounded-xl hover:border-gray-700 transition-all group"
          >
            {/* Thumbnail */}
            <div className="relative w-48 h-28 flex-shrink-0 rounded-lg overflow-hidden bg-black">
              <img 
                src={video.thumbnail} 
                alt={video.title}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div className="absolute top-2 left-2 bg-black/80 text-white text-xs px-2 py-1 rounded font-mono">
                #{index + 1}
              </div>
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0">
              <h3 className="text-lg font-semibold text-gray-100 line-clamp-2 leading-tight mb-1">
                {video.title}
              </h3>
              <p className="text-sm text-gray-400 mb-3 flex items-center gap-2">
                {video.channel_title}
              </p>
              
              <div className="flex items-center gap-3">
                {/* AI Score Badge */}
                {video.ai_score && (
                  <div className={`
                    flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium border
                    ${video.ai_score >= 80 
                      ? "bg-green-500/10 text-green-400 border-green-500/20" 
                      : video.ai_score >= 60 
                        ? "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"
                        : "bg-red-500/10 text-red-400 border-red-500/20"
                    }
                  `}>
                    <Star className="w-3.5 h-3.5 fill-current" />
                    AI Score: {video.ai_score}
                  </div>
                )}
                
                <a 
                  href={`https://www.youtube.com/watch?v=${video.video_id}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-blue-400 hover:text-blue-300 flex items-center gap-1"
                >
                  Watch <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
