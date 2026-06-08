# StudySync AI 🎓🚀

**StudySync AI** is a premium, intelligent study companion that generates personalized learning playlists for any topic. It acts as an "AI Tutor" by analyzing YouTube content and comments to curate the highest-rated videos for your learning path, while identifying key knowledge gaps in the coverage.

StudySync AI is now completely **database-free** and **login-free**, allowing you to generate dynamic learning playlists instantly!

---

## ✨ Features

- **🔍 AI-Powered Syllabus Generation**: Uses **Google Gemini 2.0 Flash** to dynamically outline a 5-to-7 concept target syllabus for any topic you enter.
- **🧠 Intelligent Sentiment Analysis**: Ranks and filters YouTube search results based on the sentiment and feedback in public comments using a Hugging Face Transformers model.
- **🧩 Semantic Gap Analysis**: Uses Sentence Transformers to evaluate the coverage of search results against the generated syllabus, detecting concepts that you need to study further.
- **💻 Premium Dark Mode UI**: A gorgeous, glassmorphic dark-theme user interface built entirely with Streamlit and styled for modern desktops.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** (UI & Frontend)
- **Google Gemini API** (Generative AI Core)
- **Hugging Face Transformers** (Sentiment Analysis)
- **Sentence Transformers** (Semantic Similarity & Embeddings)
- **YouTube Data API v3** (Content Retrieval)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+ installed.
- Google AI Studio (Gemini) API Key.
- Google Cloud Platform (YouTube Data API v3) API Key.

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/SaurabhVora/study-sync-ai.git
   cd study-sync-ai
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a `.env` file inside the `backend/` directory using the template:
   ```env
   YOUTUBE_API_KEY=your_youtube_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

4. **Launch the Application**
   Run the Streamlit server:
   ```bash
   streamlit run streamlit_app.py
   ```
   Or simply double-click the `start_app.bat` script on Windows!
