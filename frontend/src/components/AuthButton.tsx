"use client";

import { useState, useEffect } from "react";
import { supabase } from "@/lib/supabase";
import { User } from "@supabase/supabase-js";
import { LogIn, LogOut, User as UserIcon } from "lucide-react";

export function AuthButton() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check active session
    const getUser = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      setUser(session?.user ?? null);
      setLoading(false);
    };

    getUser();

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleLogin = async () => {
    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${location.origin}/auth/callback`,
      },
    });
  };

  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  if (loading) return <div className="w-8 h-8 bg-gray-800 rounded-full animate-pulse" />;

  if (user) {
    return (
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 text-sm text-gray-300">
            {user.user_metadata.avatar_url ? (
                <img src={user.user_metadata.avatar_url} className="w-8 h-8 rounded-full" alt="Avatar" />
            ) : (
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                    <UserIcon className="w-4 h-4 text-white" />
                </div>
            )}
            <span className="hidden md:inline">{user.email}</span>
        </div>
        <button
          onClick={handleLogout}
          className="p-2 hover:bg-red-500/10 text-gray-400 hover:text-red-400 rounded-lg transition-colors"
          title="Sign Out"
        >
          <LogOut className="w-5 h-5" />
        </button>
      </div>
    );
  }

  return (
    <button
      onClick={handleLogin}
      className="flex items-center gap-2 px-4 py-2 bg-white text-black rounded-full font-medium hover:bg-gray-200 transition-colors"
    >
      <LogIn className="w-4 h-4" />
      Sign In
    </button>
  );
}
