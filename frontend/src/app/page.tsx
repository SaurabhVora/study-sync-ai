"use client";

import { useState } from "react";
import { PlaylistView } from "@/components/PlaylistView";
import { AuthButton } from "@/components/AuthButton";
import { VideoResult } from "@/lib/types";
import { BookOpen, Search, Plus } from "lucide-react";

export default function Home() {
  const [selectedTopic, setSelectedTopic] = useState<string>("");
  const [videos, setVideos] = useState<VideoResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  
  // State for dynamic topics
  const [topics, setTopics] = useState<string[]>([
    "Round Robin Scheduling",
    "Bankers Algorithm",
    "Virtual Memory",
    "Semaphores in OS",
    "Page Replacement Algorithms"
  ]);
  const [searchQuery, setSearchQuery] = useState("");

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    
    // Add new topic to list if not exists
    if (!topics.includes(searchQuery)) {
        setTopics([searchQuery, ...topics]);
    }
    
    // Trigger generation
    handleTopicClick(searchQuery);
    setSearchQuery("");
  };

  const handleTopicClick = async (topic: string) => {
    setSelectedTopic(topic);
    setIsLoading(true);
    setVideos([]); // Clear previous

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/playlist/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic_name: topic, limit: 5 }),
      });
      
      const data = await res.json();
      setVideos(data.videos);
    } catch (error) {
      console.error("Failed to generate playlist", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen bg-black text-gray-100 font-sans">
      {/* Sidebar */}
      <div className="w-72 border-r border-gray-800 bg-gray-950 p-6 flex flex-col">
        <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-2 text-blue-500">
                <BookOpen className="w-6 h-6" />
                <h1 className="text-lg font-bold tracking-tight text-white">StudySync</h1>
            </div>
        </div>

        <div className="mb-6">
            <AuthButton />
        </div>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="mb-6 relative">
            <input 
                type="text" 
                placeholder="Enter any topic..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-gray-900 border border-gray-800 rounded-lg py-2 pl-3 pr-10 text-sm text-white focus:outline-none focus:border-blue-500 transition-colors"
            />
            <button 
                type="submit"
                className="absolute right-2 top-2 text-gray-400 hover:text-white"
            >
                <Plus className="w-4 h-4" />
            </button>
        </form>

        <div className="space-y-1 overflow-y-auto flex-1">
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 px-2">
            Your Topics
          </p>
          {topics.map((topic) => (
            <button
              key={topic}
              onClick={() => handleTopicClick(topic)}
              className={`
                w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all flex items-center gap-3
                ${selectedTopic === topic 
                  ? "bg-blue-600 text-white shadow-lg shadow-blue-900/20" 
                  : "text-gray-400 hover:bg-gray-900 hover:text-gray-200"
                }
              `}
            >
              <Search className="w-4 h-4 opacity-50" />
              <span className="truncate">{topic}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 bg-gray-950/50">
        <PlaylistView 
          topic={selectedTopic} 
          videos={videos} 
          isLoading={isLoading} 
        />
      </div>
    </main>
  );
}
