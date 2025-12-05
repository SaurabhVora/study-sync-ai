-- StudySync Database Schema

-- 1. Subjects Table (e.g., "Operating Systems", "DBMS")
create table subjects (
  id uuid default gen_random_uuid() primary key,
  name text not null unique,
  description text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. Units Table (e.g., "Process Management")
create table units (
  id uuid default gen_random_uuid() primary key,
  subject_id uuid references subjects(id) on delete cascade not null,
  name text not null,
  order_index integer not null, -- To keep units in syllabus order
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 3. Topics Table (e.g., "Round Robin Scheduling")
create table topics (
  id uuid default gen_random_uuid() primary key,
  unit_id uuid references units(id) on delete cascade not null,
  name text not null,
  keywords text[], -- Array of keywords for AI matching
  order_index integer not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 4. Resources Table (The actual content)
create type resource_type as enum ('youtube_video', 'pdf', 'article', 'book');

create table resources (
  id uuid default gen_random_uuid() primary key,
  topic_id uuid references topics(id) on delete cascade not null,
  title text not null,
  url text not null,
  type resource_type not null,
  
  -- AI Metadata
  quality_score float check (quality_score >= 0 and quality_score <= 100),
  clarity_score float,
  sentiment_score float,
  
  -- Source Metadata
  channel_name text, -- For YouTube
  duration_seconds integer,
  thumbnail_url text,
  
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 5. Playlists (Curated collections)
create table playlists (
  id uuid default gen_random_uuid() primary key,
  topic_id uuid references topics(id) on delete cascade not null,
  name text not null, -- e.g. "Best of Round Robin"
  is_ai_generated boolean default false,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 6. Playlist Items (Linking resources to playlists)
create table playlist_items (
  id uuid default gen_random_uuid() primary key,
  playlist_id uuid references playlists(id) on delete cascade not null,
  resource_id uuid references resources(id) on delete cascade not null,
  position integer not null,
  unique(playlist_id, position)
);
