# 🎬 Netflix Movie Finder

A semantic movie recommendation system built with RAG (Retrieval-Augmented Generation). Search for movies by vibe, mood, or description — not just keywords.

---

## 🚀 Live Demo

👉 [Coming soon on Streamlit Cloud](#)

---

## 🧠 How It Works

```
Netflix Dataset (CSV)
        ↓
Load with DataFrameLoader
        ↓
Embed descriptions with HuggingFace BGE Embeddings
        ↓
Store vectors in ChromaDB
        ↓
User query → Semantic Search → Top N movies + Netflix links
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python |
| Framework | LangChain |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | ChromaDB |
| Frontend | Streamlit |
| Dataset | Netflix Movies & TV Shows (Kaggle) |

---

## 📁 Project Structure

```
movie/
├── movie.py              # RAG pipeline class
├── app.py                # Streamlit frontend
├── netflix_titles.csv    # Netflix dataset
├── requirements.txt      # Dependencies
├── Chroma_DB/            # Auto-generated vector store
└── README.md             # You are here
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/netflix-movie-finder.git
cd netflix-movie-finder
```

### 2. Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the dataset
Get the Netflix dataset from Kaggle:
👉 [kaggle.com/datasets/shivamb/netflix-shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

Place `netflix_titles.csv` in the project root.

### 5. Run the app
```bash
streamlit run app.py
```

> **Note:** First run will take 5–15 minutes to build the vector database. Subsequent runs load in seconds.

---

## 💡 Usage

1. Type a mood, vibe, or description in the search bar
2. Select number of results
3. Click **Find Movies**
4. Click **▶ Watch on Netflix** to open the movie directly

### Example queries
```
"a dark thriller with unexpected plot twists"
"romantic movie with a sad ending"
"comedy about family drama in Africa"
"sci-fi with time travel and mind-bending story"
"feel-good movie to watch on a Sunday"
```

---

## 📦 Requirements

```
streamlit
pandas
langchain
langchain-community
langchain-chroma
langchain-text-splitters
sentence-transformers
chromadb
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🚀 Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to 👉 [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file as `app.py`
5. Click **Deploy**

---

## 🙋‍♂️ Author

**KC (Kenechukwu Emmanuel Nduaguba)**
Full-Stack Developer & AI Automation Engineer

- GitHub: [@nduprincekc](https://github.com/nduprincekc)
- Twitter/X: [@nduagubakc](https://twitter.com/nduagubakc)
- LinkedIn: [linkedin.com/in/nduagubakc](https://linkedin.com/in/nduagubakc)

---



## 📄 License

MIT License — free to use and modify.