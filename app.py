import streamlit as st
import pandas as pd
from movie import movie_rag
import os

st.set_page_config(
    page_title="Netflix Movie Finder",
    page_icon="🎬",
    layout="wide"
)

# ── Custom CSS ───────────────────────────────
st.markdown("""
<style>
    body { background-color: #141414; }
    .main { background-color: #141414; }

    .movie-card {
        background-color: #1f1f1f;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #333;
        transition: 0.3s;
    }
    .movie-card:hover {
        border: 1px solid #e50914;
    }
    .movie-title {
        color: #ffffff;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .movie-meta {
        color: #aaaaaa;
        font-size: 13px;
        margin-bottom: 10px;
    }
    .movie-description {
        color: #cccccc;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 14px;
    }
    .watch-btn {
        background-color: #e50914;
        color: white !important;
        padding: 8px 18px;
        border-radius: 6px;
        text-decoration: none !important;
        font-weight: bold;
        font-size: 14px;
    }
    .watch-btn:hover {
        background-color: #b20710;
    }
    h1, h2, h3, p, label {
        color: #ffffff !important;
    }
    .stTextInput input {
        background-color: #2b2b2b;
        color: white;
        border: 1px solid #444;
        border-radius: 8px;
    }
    .stButton button {
        background-color: #e50914;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 28px;
        font-weight: bold;
        font-size: 16px;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #b20710;
    }
    .stSlider { color: white; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 40px 0 20px 0;'>
    <h1 style='font-size:48px; color:#e50914;'>🎬 Netflix Movie Finder</h1>
    <p style='color:#aaaaaa; font-size:18px;'>Describe a vibe, mood, or story — we'll find your next watch</p>
</div>
""", unsafe_allow_html=True)

# ── Load RAG ─────────────────────────────────
@st.cache_resource
def load_rag():
    df = pd.read_csv("netflix_titles.csv")
    df.dropna(subset=["description"], inplace=True)
    rag = movie_rag(df=df, device="cpu")
    if not os.path.exists("Chroma_DB"):
        with st.spinner("⚙️ Building database... first time only"):
            rag.create_vector_database()
    return rag

rag = load_rag()

# ── Search Bar ───────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input(
        "",
        placeholder="e.g. a dark thriller with unexpected plot twists...",
        label_visibility="collapsed"
    )
with col2:
    k = st.selectbox("Results", [3, 5, 8, 10], index=1)

search = st.button("🔍 Find Movies")

# ── Results ──────────────────────────────────
if search and query:
    with st.spinner("🎬 Finding your perfect watch..."):
        results = rag.get_movie(query, k=k)

    st.markdown(f"""
    <div style='text-align:center; padding: 20px 0;'>
        <h3>Top {k} results for: <span style='color:#e50914;'>{query}</span></h3>
    </div>
    """, unsafe_allow_html=True)

    # Display in 3-column grid
    cols = st.columns(3)
    for i, movie in enumerate(results):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='movie-card'>
                <div class='movie-title'>🎬 {movie['title']}</div>
                <div class='movie-meta'>
                    {movie.get('type', 'Movie')} &nbsp;•&nbsp;
                    {movie.get('release_year', '')} &nbsp;•&nbsp;
                    {movie.get('rating', '')}
                </div>
                <div class='movie-description'>
                    {movie['description'][:200]}...
                </div>
                <a href='{movie['link']}' target='_blank' class='watch-btn'>
                    ▶ Watch on Netflix
                </a>
            </div>
            """, unsafe_allow_html=True)