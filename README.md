# StudySync AI 🎓🚀

**StudySync AI** is an intelligent study companion that generates personalized video playlists for any topic. It acts as an "AI Tutor" by analyzing thousands of YouTube videos to curate the best learning path for you.

## ✨ Features

- **🔍 AI-Powered Search**: Generates playlists by analyzing YouTube videos.
- **🧠 Sentiment Analysis**: Ranks videos based on comment quality (filters out clickbait).
- **🧩 Generative Syllabus**: Uses **Google Gemini 1.5 Flash** to create a dynamic syllabus for _any_ topic (e.g., "Machine Learning", "Quantum Physics").
- **📚 My Library**: Save your favorite playlists to Supabase.
- **🎯 Gap Analysis**: Compares the video content against the "Ideal Syllabus" to tell you what you are missing.

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** (UI & Frontend)
- **Google Gemini API** (Generative AI)
- **Hugging Face Transformers** (Sentiment Analysis)
- **Sentence Transformers** (Semantic Similarity)
- **Supabase** (Database)

## 🚀 Getting Started

### Prerequisites

- Python 3.9+ installed.
- Supabase Account.
- Google AI Studio API Key.

### Installation

1.  **Clone the repo**

    ```bash
    git clone https://github.com/yourusername/study-sync-ai.git
    cd study-sync-ai
    ```

2.  **Setup Backend**

    ```bash
    cd backend
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate

    pip install -r requirements.txt
    ```

3.  **Environment Variables**
    Create a `.env` file in `backend/` with the following:

    ```env
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_anon_key
    YOUTUBE_API_KEY=your_youtube_api_key
    GEMINI_API_KEY=your_gemini_api_key
    ```

4.  **Run the App**
    Double-click `start_app.bat` (Windows) or run:
    ```bash
    streamlit run streamlit_app.py
    ```

## 📸 Screenshots

_(Add your screenshots here)_

## 🤝 Contributing

Pull requests are welcome.

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)
