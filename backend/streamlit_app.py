import streamlit as st
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set Page Config (Must be first)
st.set_page_config(
    page_title="StudySync AI - Your Intelligent Study Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Premium Design System
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;600&display=swap');

/* Apply font families */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Inter', sans-serif !important;
}
h1, h2, h3, h4, h5, h6, .gradient-title {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
}

/* Background gradient and styling */
.stApp {
    background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 70%, #020617 100%) !important;
    color: #f8fafc !important;
}

/* Main title styling */
.gradient-title {
    background: linear-gradient(135deg, #c084fc 0%, #6366f1 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.5rem !important;
    text-align: center;
    margin-bottom: 0.2rem !important;
    letter-spacing: -1.5px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1.25rem;
    margin-bottom: 3rem;
    font-weight: 300;
}

/* Hide sidebar and streamline UI */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Glassmorphism containers and inputs */
div[data-baseweb="input"] {
    background-color: rgba(30, 41, 59, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 14px !important;
    transition: all 0.3s ease !important;
    padding: 4px 8px !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: #818cf8 !important;
    box-shadow: 0 0 20px rgba(129, 140, 248, 0.25) !important;
}

/* Premium Primary Buttons */
button[kind="primary"] {
    background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%) !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 12px 32px !important;
    color: white !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    font-family: 'Outfit', sans-serif !important;
    box-shadow: 0 4px 20px rgba(168, 85, 247, 0.35) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100% !important;
}

button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(168, 85, 247, 0.5) !important;
}

/* Custom styled cards for video containers */
div[data-testid="stForm"] {
    background: rgba(30, 41, 59, 0.45) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 20px !important;
    padding: 30px !important;
    backdrop-filter: blur(16px);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25) !important;
}

.video-container {
    background: rgba(30, 41, 59, 0.3) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    margin-bottom: 20px !important;
    transition: all 0.3s ease !important;
    backdrop-filter: blur(12px);
}

.video-container:hover {
    background: rgba(30, 41, 59, 0.5) !important;
    border-color: rgba(129, 140, 248, 0.3) !important;
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(99, 102, 241, 0.15) !important;
}

/* Info and success boxes styling */
div[data-testid="stNotification"] {
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(8px);
}

/* Badge styling for score representation */
.badge-container {
    margin-top: 8px;
    margin-bottom: 8px;
}
.score-badge {
    background: rgba(129, 140, 248, 0.1);
    color: #818cf8;
    border: 1px solid rgba(129, 140, 248, 0.2);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# Import Services (Cached to prevent reloading models)
@st.cache_resource
def load_services():
    from app.services.youtube import youtube_service
    from app.services.ai_sentiment import sentiment_service
    from app.services.gap_filler import gap_filler_service
    from app.services.gemini_service import gemini_service
    return youtube_service, sentiment_service, gap_filler_service, gemini_service

# Load services
try:
    with st.spinner("🚀 Initializing StudySync AI Models... (This happens only once)"):
        from app.services.youtube import youtube_service
        from app.services.ai_sentiment import sentiment_service
        from app.services.gap_filler import gap_filler_service
        from app.services.gemini_syllabus import gemini_service
except Exception as e:
    st.error(f"Failed to load services: {e}")
    st.stop()

# --- Header Area ---
st.markdown('<div class="gradient-title">StudySync AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your Login-Free, Intelligent AI Study Playlist Generator</div>', unsafe_allow_html=True)

if 'search_query' not in st.session_state:
    st.session_state.search_query = "Machine Learning"

# --- Main Search Section (Centered via columns) ---
col_space1, col_form, col_space2 = st.columns([0.15, 0.7, 0.15])

with col_form:
    with st.form("search_form"):
        topic_input = st.text_input("What do you want to learn today?", value=st.session_state.search_query, placeholder="Enter any topic e.g. Quantum Computing, React JS, World War II")
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Generative Study Plan", type="primary")

if (submitted and topic_input) or ('auto_run_query' in st.session_state and st.session_state.auto_run_query):
    # Retrieve topic
    if submitted and topic_input:
        st.session_state.search_query = topic_input
        topic = topic_input
    else:
        topic = st.session_state.auto_run_query
        st.session_state.auto_run_query = None # clear

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    with st.status(f"🔍 Curating plan for '{topic}'...", expanded=True) as status:
        # 1. Gemini Syllabus
        status.write("🧠 Consulting Gemini AI for optimal syllabus...")
        required_topics = gemini_service.generate_syllabus(topic)
        
        # 2. YouTube Search
        status.write("🎥 Searching YouTube for high-quality content...")
        raw_videos = youtube_service.search_videos(topic, max_results=10)
        
        # 3. Process Videos (Sentiment + Gaps)
        status.write("🤖 Analyzing video reviews & content coverage...")
        processed_videos = []
        video_titles = []
        
        progress_bar = st.progress(0)
        for i, vid in enumerate(raw_videos):
            score = 50.0
            comments = youtube_service.get_video_comments(vid['video_id'])
            if comments:
                score = sentiment_service.analyze_comments(comments)
            
            vid['ai_score'] = score
            processed_videos.append(vid)
            video_titles.append(vid['title'])
            progress_bar.progress((i + 1) / len(raw_videos))
            
        # Sort by AI Score
        processed_videos.sort(key=lambda x: x['ai_score'], reverse=True)
        
        # Gap Analysis
        gaps = gap_filler_service.find_gaps(video_titles, required_topics)
        
        status.update(label="✅ Plan successfully generated!", state="complete", expanded=False)

    # --- Render Targets ---
    if required_topics:
        st.markdown(f"### 🎯 Recommended Learning Path for **{topic}**")
        st.write(f"**Target syllabus concepts:** {', '.join(required_topics)}")
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # Layout: 2 Columns (Videos Left, Gaps Right)
    left_col, right_col = st.columns([0.65, 0.35])
    
    with left_col:
        st.markdown("### 📺 Handpicked Video Recommendations")
        if not processed_videos:
            st.warning("No videos could be retrieved for this topic. Please check your YouTube API Key or quota.")
        else:
            for vid in processed_videos[:5]:
                # Wrap each video inside our custom styled CSS video-container
                with st.container():
                    st.markdown('<div class="video-container">', unsafe_allow_html=True)
                    c1, c2 = st.columns([0.35, 0.65])
                    c1.image(vid['thumbnail'], use_container_width=True)
                    
                    c2.markdown(f"#### **[{vid['title']}](https://www.youtube.com/watch?v={vid['video_id']})**")
                    c2.markdown(f"👤 *Channel:* `{vid['channel_title']}`")
                    
                    # Custom Badged AI Score
                    score = vid['ai_score']
                    color = "#10b981" if score > 70 else "#f59e0b" if score > 50 else "#ef4444"
                    c2.markdown(f"""
                    <div class="badge-container">
                        <span class="score-badge" style="color: {color}; border-color: {color}aa; background: {color}1a;">
                            🧠 AI Score: {score:.1f}%
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with c2.expander("Show Description"):
                        st.caption(vid['description'][:300] + ("..." if len(vid['description']) > 300 else ""))
                    st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown("### 🧩 Syllabus Concept Coverage")
        if gaps:
            st.warning("Concept Gaps Detected:")
            st.info("The recommended videos above might not cover the following prerequisites thoroughly. We recommend searching them separately:")
            for g in gaps:
                # Button to automatically trigger search for that gap
                if st.button(f"🔍 Learn Concept: {g}", key=f"gap_{g}", use_container_width=True):
                    st.session_state.auto_run_query = g
                    st.session_state.search_query = g
                    st.rerun()
        else:
            st.success("Reference coverage is excellent! The top recommendations cover all target topics well.")
