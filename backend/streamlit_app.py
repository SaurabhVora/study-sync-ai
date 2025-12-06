import streamlit as st
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set Page Config (Must be first)
st.set_page_config(
    page_title="StudySync AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import Services (Cached to prevent reloading models)
@st.cache_resource
def load_services():
    from app.services.youtube import youtube_service
    from app.services.ai_sentiment import sentiment_service
    from app.services.gap_filler import gap_filler_service
    from app.services.gemini_syllabus import gemini_service
    from app.core.supabase import supabase
    return youtube_service, sentiment_service, gap_filler_service, gemini_service, supabase

# Load services
try:
    with st.spinner("🚀 Loading AI Models... (This happens only once)"):
        youtube_service, sentiment_service, gap_filler_service, gemini_service, supabase = load_services()
except Exception as e:
    st.error(f"Failed to load services: {e}")
    st.stop()

# --- Sidebar: User & Library ---
with st.sidebar:
    st.title("🎓 StudySync AI")
    
    # Simple Auth
    if 'user' not in st.session_state:
        st.session_state.user = None

    if not st.session_state.user:
        with st.expander("🔐 Login / Signup", expanded=True):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            action = st.radio("Action", ["Login", "Sign Up"])
            
            if st.button("Submit"):
                try:
                    if action == "Login":
                        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    else:
                        res = supabase.auth.sign_up({"email": email, "password": password})
                    
                    if res.user:
                        st.session_state.user = res.user
                        st.success(f"Welcome, {email}!")
                        st.rerun()
                except Exception as e:
                    st.error(str(e))
    else:
        st.write(f"👤 **{st.session_state.user.email}**")
        if st.button("Logout"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

        st.divider()
        st.subheader("📚 My Library")

        # Fetch Playlists
        try:
            res = supabase.table("playlists").select("*").eq("user_id", st.session_state.user.id).order("created_at", desc=True).execute()
            saved_playlists = res.data
            
            if not saved_playlists:
                st.caption("No saved playlists yet.")
            
            for pl in saved_playlists:
                col1, col2 = st.columns([0.8, 0.2])
                if col1.button(pl['name'], key=f"load_{pl['id']}"):
                    st.session_state.search_query = pl['name']
                    st.rerun()
                if col2.button("🗑️", key=f"del_{pl['id']}"):
                    supabase.table("playlist_items").delete().eq("playlist_id", pl['id']).execute()
                    supabase.table("playlists").delete().eq("id", pl['id']).execute()
                    st.rerun()

        except Exception as e:
            st.error(f"Error loading library: {e}")

# --- Main Content ---
st.title("Resource Aggregator")
st.caption("Powered by Gemini 1.5 Flash & Semantic Search")

if 'search_query' not in st.session_state:
    st.session_state.search_query = "Machine Learning"

# Search Form
with st.form("search_form"):
    topic_input = st.text_input("Enter a topic to learn:", value=st.session_state.search_query)
    submitted = st.form_submit_button("Generative Study Plan", type="primary")

if submitted and topic_input:
    st.session_state.search_query = topic_input
    topic = topic_input

    with st.status(f"🔍 Analyzing '{topic}'...", expanded=True) as status:
        
        # 1. Gemini Syllabus
        status.write("🧠 Consulting Gemini for syllabus...")
        required_topics = gemini_service.generate_syllabus(topic)
        st.write(f"**Target Syllabus:** {', '.join(required_topics)}")
        
        # 2. YouTube Search
        status.write("🎥 Searching YouTube...")
        raw_videos = youtube_service.search_videos(topic, max_results=10)
        
        # 3. Process Videos (Sentiment + Gaps)
        status.write("🤖 Analyzing Sentiment & Gaps...")
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
        
        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

    # --- Display Results ---
    
    # Save Button
    if st.session_state.user:
        col_head, col_save = st.columns([0.8, 0.2])
        if col_save.button("💾 Save to Library"):
            try:
                # 1. Insert Playlist
                pl_data = {
                    "user_id": st.session_state.user.id,
                    "name": topic,
                    "description": f"AI Playlist for {topic}"
                }
                pl_res = supabase.table("playlists").insert(pl_data).execute()
                pl_id = pl_res.data[0]['id']
                
                # 2. Insert Items
                items = []
                for i, v in enumerate(processed_videos[:5]):
                     items.append({
                        "playlist_id": pl_id,
                        "video_id": v['video_id'],
                        "title": v['title'],
                        "url": f"https://www.youtube.com/watch?v={v['video_id']}",
                        "position": i
                    })
                supabase.table("playlist_items").insert(items).execute()
                st.toast("Playlist Saved Successfully!", icon="✅")
                st.rerun() # Refresh sidebar
            except Exception as e:
                st.error(f"Save failed: {e}")

    # Layout: 2 Columns
    left_col, right_col = st.columns([0.7, 0.3])
    
    with left_col:
        st.subheader(f"📺 Top Videos for {topic}")
        for vid in processed_videos[:5]:
            with st.container(border=True):
                c1, c2 = st.columns([0.4, 0.6])
                c1.image(vid['thumbnail'], use_container_width=True)
                c2.markdown(f"**[{vid['title']}](https://www.youtube.com/watch?v={vid['video_id']})**")
                c2.caption(f"Channel: {vid['channel_title']}")
                
                # AI Badge
                score = vid['ai_score']
                color = "green" if score > 70 else "orange" if score > 50 else "red"
                c2.markdown(f"🧠 AI Score: :{color}[**{score:.1f}**]")
                with st.expander("Description"):
                    st.text(vid['description'][:200] + "...")

    with right_col:
        st.subheader("🧩 Knowledge Gaps")
        if gaps:
            st.warning(f"These concepts might be missing from the videos above:")
            for g in gaps:
                st.info(f"**{g}**")
                if st.button(f"Find '{g}'", key=f"gap_{g}"):
                    st.session_state.search_query = g
                    st.rerun()
        else:
            st.success("Reference coverage looks great!")

