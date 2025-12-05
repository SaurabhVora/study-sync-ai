# StudySync - Implementation Plan

## 1. Project Overview

**StudySync** is an AI-powered educational aggregator that curates the "Perfect Playlist" for students by analyzing content quality, filling gaps, and personalizing recommendations.

## 2. Tech Stack

- **Frontend**: Next.js (React) + Tailwind CSS + Framer Motion (Hybrid SSR/CSR)
- **Backend**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **AI/ML**:
  - `sentence-transformers` (Semantic Search)
  - `transformers` (Sentiment Analysis)
  - Groq API (Summarization)
- **Data Sources**: YouTube Data API v3, NPTEL Scrapers

## 3. Architecture

- **/frontend**: Next.js application handling UI, Authentication (Supabase Auth), and display logic.
- **/backend**: Python API handling data fetching, AI processing, and complex logic.
- **/documentation**: Project docs, plans, and schemas.

## 4. Development Phases

### Phase 1: Foundation & Syllabus

- Set up project structure.
- Define Database Schema (Subjects, Units, Topics).
- Create the "Master Syllabus" JSON/DB entries.

### Phase 2: The Harvester (Backend)

- Implement YouTube Data API client.
- Create the "Gap Filling" logic.
- Implement basic Sentiment Analysis on comments.

### Phase 3: The Interface (Frontend)

- Build the Syllabus Tree navigation.
- Build the Video Player & Playlist UI.
- Integrate with Backend API.

### Phase 4: Polish & AI

- Improve AI ranking with vector embeddings.
- Add User Accounts (Save playlists).
- "Gap Filled" badges and UI polish.
