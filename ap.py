import streamlit as st
import pandas as pd
from movie import movie_rag
import os

st.set_page_config(
    page_title="🎬 Movie Finder",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Netflix Movie Finder")
st.markdown("Search for movies by vibe, mood, or description")

# ── Load & Cache Everything ──────────────────
@st.cache_resource
def load_rag():
    df = pd.read_csv("netflix_titles.csv")
    df.dropna(subset=["description"], inplace=True)
    rag = movie_rag(df=df, device="cpu")

    if not os.path.exists("Chroma_DB"):
        with st.spinner("Building movie database... (first time only)"):
            rag.create_vector_database()
    return rag

rag = load_rag()

# ── Search UI ────────────────────────────────
query = st.text_input(
    "What kind of movie are you looking for?",
    placeholder="e.g. romantic movie with a sad ending..."
)

k = st.slider("Number of results", min_value=1, max_value=10, value=5)

if st.button("🔍 Search") and query:
    with st.spinner("Searching..."):
        results = rag.get_movie(query, k=k)

    st.markdown(f"### Top {k} Results for: *{query}*")
    st.divider()

    for i, doc in enumerate(results, 1):
        # Parse the combined content
        parts = doc.page_content.split(" | ")
        title = parts[0] if len(parts) > 0 else "Unknown"
        description = parts[-1] if len(parts) > 1 else doc.page_content

        with st.container():
            st.markdown(f"**{i}. {title}**")
            st.write(description[:300] + "...")
            st.divider()