import streamlit as st
import pandas as pd
from movie import movie_rag
import os

st.set_page_config(
    page_title="Netflix Movie Finder",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    html, body, [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"], section.main, .main,
    [data-testid="stHeader"], [data-testid="stSidebar"] {
        background-color: #141414 !important;
        color: #ffffff !important;
    }
    .block-container { padding-top: 2rem !important; background-color: #141414 !important; }
    .stTextInput input {
        background-color: #2b2b2b !important;
        color: white !important;
        border: 1px solid #e50914 !important;
        border-radius: 8px !important;
    }
    .stButton button {
        background-color: #e50914 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 28px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        width: 100% !important;
    }
    .stButton button:hover { background-color: #b20710 !important; }
    .movie-card {
        background-color: #1f1f1f;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #333;
    }
    .movie-card:hover { border: 1px solid #e50914; }
    .movie-title { color: #ffffff; font-size: 18px; font-weight: bold; margin-bottom: 6px; }
    .movie-meta { color: #aaaaaa; font-size: 12px; margin-bottom: 10px; }
    .movie-description { color: #cccccc; font-size: 13px; line-height: 1.6; margin-bottom: 14px; }
    .watch-btn {
        background-color: #e50914;
        color: white !important;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none !important;
        font-weight: bold;
        font-size: 13px;
    }
    h1, h2, h3, h4, h5, p, label, span { color: #ffffff !important; }
    hr { border-color: #333 !important; }
</style>
""", unsafe_allow_html=True)


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

# ── Header ───────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 30px 0 20px 0;'>
    <h1 style='font-size:48px; color:#e50914;'>🎬 Netflix Movie Finder</h1>
    <p style='color:#aaaaaa; font-size:18px;'>
        Describe a vibe, mood, or story — we'll find your next watch
    </p>
</div>
""", unsafe_allow_html=True)

# ── Search ───────────────────────────────────
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

    if not results:
        st.warning("No results found. Try a different query.")
    else:
        st.markdown(f"""
        <div style='text-align:center; padding:16px 0;'>
            <h3>Top {len(results)} results for:
                <span style='color:#e50914;'>{query}</span>
            </h3>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        for i, movie in enumerate(results):
            with cols[i % 3]:
                st.markdown(f"""
                <div class='movie-card'>
                    <div class='movie-title'>🎬 {movie['title']}</div>
                    <div class='movie-meta'>
                        {movie.get('type', '')} &nbsp;•&nbsp;
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