"use client";

import { useState, useEffect } from "react";
import { PlaylistView } from "@/components/PlaylistView";
import { AuthButton } from "@/components/AuthButton";
import { VideoResult } from "@/lib/types";
import { BookOpen, Search, Plus, Library, Trash2 } from "lucide-react";
import { supabase } from "@/lib/supabase";
import { User } from "@supabase/supabase-js";

interface SavedPlaylist {
    id: string;
    user_id: string;
    name: string;
    description: string;
    created_at: string;
}

export default function Home() {
  const [user, setUser] = useState<User | null>(null);
  const [selectedTopic, setSelectedTopic] = useState<string>("");
  const [videos, setVideos] = useState<VideoResult[]>([]);
  const [gaps, setGaps] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  
  // Saved Playlists
  const [savedPlaylists, setSavedPlaylists] = useState<SavedPlaylist[]>([]);

  // State for dynamic topics
  const [topics, setTopics] = useState<string[]>([
    "Round Robin Scheduling",
    "Bankers Algorithm",
    "Virtual Memory",
    "Semaphores in OS",
    "Page Replacement Algorithms"
  ]);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    // Check auth and fetch saved playlists
    const init = async () => {
        const { data: { session } } = await supabase.auth.getSession();
        setUser(session?.user ?? null);
        if (session?.user) {
            fetchSavedPlaylists(session.user.id);
        }
    };
    init();

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
        setUser(session?.user ?? null);
        if (session?.user) {
            fetchSavedPlaylists(session.user.id);
        } else {
            setSavedPlaylists([]);
        }
    });
    return () => subscription.unsubscribe();
  }, []);

  const fetchSavedPlaylists = async (userId: string) => {
      try {
          const res = await fetch(`http://127.0.0.1:8000/api/v1/playlist/user/${userId}`);
          const data = await res.json();
          setSavedPlaylists(data);
      } catch (err) {
          console.error("Failed to fetch saved playlists", err);
      }
  };

  const handleSavePlaylist = async () => {
      if (!user) {
          alert("Please sign in to save playlists!");
          return;
      }
      setIsSaving(true);
      try {
          const res = await fetch("http://127.0.0.1:8000/api/v1/playlist/save", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                  user_id: user.id,
                  topic_name: selectedTopic,
                  videos: videos
              })
          });
          if (res.ok) {
              alert("Playlist saved to library!");
              fetchSavedPlaylists(user.id);
          } else {
              alert("Failed to save playlist.");
          }
      } catch (err) {
          console.error(err);
          alert("Error saving playlist.");
      } finally {
          setIsSaving(false);
      }
  };

  const handleDeletePlaylist = async (id: string, e: React.MouseEvent) => {
      e.stopPropagation(); // Prevent opening the playlist when clicking delete
      if (!confirm("Are you sure you want to delete this playlist?")) return;
      
      try {
          const res = await fetch(`http://127.0.0.1:8000/api/v1/playlist/${id}`, { method: "DELETE" });
          if (res.ok) {
              if (user) await fetchSavedPlaylists(user.id);
          } else {
              console.error("Failed to delete");
          }
      } catch (err) {
          console.error(err);
      }
  };

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
    setGaps([]);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/playlist/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic_name: topic, limit: 5 }),
      });
      
      const data = await res.json();
      setVideos(data.videos);
      setGaps(data.gaps || []);
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

        <div className="space-y-6 overflow-y-auto flex-1">
          {/* Saved Playlists Section */}
          {user && savedPlaylists.length > 0 && (
              <div>
                  <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 px-2 flex items-center gap-2">
                      <Library className="w-3 h-3" /> My Library
                  </p>
                  <div className="space-y-1">
                      {savedPlaylists.map((pl) => (
                          <div key={pl.id} className="group flex items-center justify-between px-3 py-2.5 rounded-lg hover:bg-gray-900 transition-colors">
                              <button 
                                  onClick={() => handleTopicClick(pl.name)} // For now, re-generate. Ideally fetch saved items.
                                  className="text-sm text-gray-300 truncate hover:text-white text-left flex-1"
                              >
                                  {pl.name}
                              </button>
                              <button 
                                  onClick={(e) => handleDeletePlaylist(pl.id, e)}
                                  className="text-gray-600 hover:text-red-500 transition-colors px-2"
                              >
                                  <Trash2 className="w-4 h-4" />
                              </button>
                          </div>
                      ))}
                  </div>
              </div>
          )}

          {/* Popular Topics Section */}
          <div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3 px-2">
                Explore Topics
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
      </div>

      {/* Main Content */}
      <div className="flex-1 bg-gray-950/50">
        <PlaylistView 
          topic={selectedTopic} 
          videos={videos} 
          gaps={gaps}
          isLoading={isLoading}
          onSave={videos.length > 0 ? handleSavePlaylist : undefined}
          isSaving={isSaving}
        />
      </div>
    </main>
  );
}
