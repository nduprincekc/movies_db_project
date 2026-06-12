import pandas as pd
from langchain_community.document_loaders import DataFrameLoader
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


class movie_rag:
    def __init__(self, df=None, device=None, main_column="description", chroma_path="Chroma_DB"):
        self.df = df
        self.main_column = main_column
        self.chroma_path = chroma_path
        self.device = device if device else "cpu"
        self.embedding = HuggingFaceBgeEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': self.device}
        )

    def create_vector_database(self):
        loader = DataFrameLoader(self.df, page_content_column=self.main_column)
        documents = loader.load()

        for i, doc in enumerate(documents):
            row = self.df.iloc[i]
            doc.metadata["title"] = str(row.get("title", "Unknown"))
            doc.metadata["type"] = str(row.get("type", ""))
            doc.metadata["release_year"] = str(row.get("release_year", ""))
            doc.metadata["rating"] = str(row.get("rating", ""))
            doc.metadata["genre"] = str(row.get("listed_in", ""))

        reviews_vector_db = Chroma.from_documents(
            documents, self.embedding, persist_directory=self.chroma_path
        )
        return reviews_vector_db

    def load_vector_database(self):
        return Chroma(
            persist_directory=self.chroma_path,
            embedding_function=self.embedding
        )

    def get_movie(self, question, k=5):
        vector_db = self.load_vector_database()
        relevant_docs = vector_db.similarity_search(question, k=k)

        results = []
        for doc in relevant_docs:
            title = doc.metadata.get("title", "Unknown")
            link = f"https://www.netflix.com/search?q={title.replace(' ', '%20')}"
            results.append({
                "title": title,
                "description": doc.page_content,
                "link": link,
                "type": doc.metadata.get("type", ""),
                "release_year": doc.metadata.get("release_year", ""),
                "rating": doc.metadata.get("rating", ""),
                "genre": doc.metadata.get("genre", ""),
            })
        return results