# StudySync AI 🎓🚀

**StudySync AI** is an intelligent study companion that generates personalized video playlists for any topic. It uses AI to analyze YouTube video comments for quality (sentiment analysis) and identifies "knowledge gaps" in the curriculum to suggest prerequisite topics.

## ✨ Features

- **🔍 AI-Powered Search**: Generates playlists by analyzing YouTube videos.
- **🧠 Sentiment Analysis**: Ranks videos based on user sentiment in comments (filters out clickbait).
- **🧩 Gap Analysis**: Identifies missing prerequisite topics (currently optimized for Operating Systems).
- **📂 My Library**: Save your favorite playlists to your personal library (stored in Supabase).
- **🗑️ Manage Content**: Delete playlists you no longer need.
- **🔐 Authentication**: Secure user login via Supabase.

## 🛠️ Tech Stack

### Frontend

- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS** (for styling)
- **Lucide React** (for icons)
- **Supabase Auth** (for user management)

### Backend

- **FastAPI** (Python)
- **Youtube v3 API** (Data fetching)
- **Hugging Face Transformers** (Sentiment Analysis)
- **Sentence Transformers** (Gap Analysis embeddings)
- **Supabase** (Database & Storage)

## 🚀 Getting Started

### Prerequisites

- Node.js & npm
- Python 3.9+
- Supabase Account
- Google Cloud Project (for YouTube Data API)

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 3. Environment Variables

Create `.env` in `backend/` and `.env.local` in `frontend/` with your API keys (Supabase, YouTube, etc.).

## 📸 Screenshots

_(Add your screenshots here)_

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)
