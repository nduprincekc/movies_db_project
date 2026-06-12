import streamlit as st
import pandas as pd
from movie import movie_rag
import os

TMDB_API_KEY = "your_tmdb_api_key_here"

st.set_page_config(
    page_title="Movie Finder",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    html, body, [data-testid="stApp"],
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    section.main, .main,
    [data-testid="stHeader"],
    [data-testid="stSidebar"] {
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
    .stSelectbox div[data-baseweb="select"] {
        background-color: #2b2b2b !important;
        color: white !important;
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
    .source-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .watch-btn {
        background-color: #e50914;
        color: white !important;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none !important;
        font-weight: bold;
        font-size: 13px;
    }
    h1, h2, h3, h4, h5, p, label, span {
        color: #ffffff !important;
    }
    hr { border-color: #333 !important; }
    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
        border-right: 1px solid #333 !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Source badge colors ──────────────────────
def badge(source):
    colors = {
        "Netflix": "#e50914",
        "Nollywood": "#008751",
        "K-Drama": "#003478"
    }
    color = colors.get(source, "#555")
    return f"<span class='source-badge' style='background-color:{color};'>{source}</span>"


# ── Load & Cache RAG ─────────────────────────
@st.cache_resource
def load_rag():
    # Load Netflix
    netflix_df = movie_rag.load_netflix_data("netflix_titles.csv")

    # Fetch Nigerian + Korean movies
    nigerian_df = movie_rag.fetch_tmdb_movies(
        TMDB_API_KEY, country_code="NG", source_label="Nollywood", pages=10
    )
    korean_df = movie_rag.fetch_tmdb_movies(
        TMDB_API_KEY, country_code="KR", source_label="K-Drama", pages=10
    )

    # Combine all
    combined_df = movie_rag.combine_datasets(netflix_df, nigerian_df, korean_df)

    print(f"✅ Netflix: {len(netflix_df)} | Nollywood: {len(nigerian_df)} | K-Drama: {len(korean_df)}")
    print(f"✅ Total: {len(combined_df)}")

    rag = movie_rag(df=combined_df, device="cpu")

    if not os.path.exists("Chroma_DB"):
        with st.spinner("⚙️ Building database... first time only, please wait"):
            rag.create_vector_database()

    return rag


rag = load_rag()

# ── Sidebar Filters ──────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.markdown("---")

    source_filter = st.radio(
        "🎬 Movie Source",
        options=["All", "Netflix", "Nollywood", "K-Drama"],
        index=0
    )

    k = st.selectbox("📊 Number of Results", [3, 5, 8, 10], index=1)

    st.markdown("---")
    st.markdown("""
    <div style='color:#aaaaaa; font-size:12px;'>
        <b>Sources:</b><br>
        🔴 Netflix — Global streaming<br>
        🟢 Nollywood — Nigerian cinema<br>
        🔵 K-Drama — Korean cinema
    </div>
    """, unsafe_allow_html=True)

# ── Header ───────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 30px 0 20px 0;'>
    <h1 style='font-size:48px; color:#e50914;'>🎬 Movie Finder</h1>
    <p style='color:#aaaaaa; font-size:18px;'>
        Netflix • Nollywood • K-Drama — Search by vibe, mood, or story
    </p>
</div>
""", unsafe_allow_html=True)

# ── Search Bar ───────────────────────────────
query = st.text_input(
    "",
    placeholder="e.g. a romantic story with unexpected betrayal...",
    label_visibility="collapsed"
)

search = st.button("🔍 Find Movies")

# ── Results ──────────────────────────────────
if search and query:
    with st.spinner("🎬 Finding your perfect watch..."):
        results = rag.get_movie(query, k=k, source_filter=source_filter)

    if not results:
        st.warning("No results found. Try a different query or filter.")
    else:
        st.markdown(f"""
        <div style='text-align:center; padding:16px 0;'>
            <h3>Top {len(results)} results for:
                <span style='color:#e50914;'>{query}</span>
                {"— " + source_filter if source_filter != "All" else ""}
            </h3>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        for i, movie in enumerate(results):
            with cols[i % 3]:
                st.markdown(f"""
                <div class='movie-card'>
                    {badge(movie['source'])}
                    <div class='movie-title'>{movie['title']}</div>
                    <div class='movie-meta'>
                        {movie.get('type', 'Movie')} &nbsp;•&nbsp;
                        {movie.get('release_year', '')} &nbsp;•&nbsp;
                        {movie.get('rating', '')}
                    </div>
                    <div class='movie-description'>
                        {movie['description'][:200]}...
                    </div>
                    <a href='{movie['link']}' target='_blank' class='watch-btn'>
                        ▶ Watch Now
                    </a>
                </div>
                """, unsafe_allow_html=True)