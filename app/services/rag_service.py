import chromadb
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class RagService:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        self.chroma = chromadb.PersistentClient(path=settings.chroma_path)

        self.collection = self.chroma.get_collection("knowledge_base")

    def query(self, question: str, top_k: int = 3):
        query_embedding = self.embedding_model.encode(question).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        docs = results["documents"][0]
        metas = results["metadatas"][0]

        context = "\n\n".join(docs)

        return context, metas


# Lazy singleton
_rag_service = None


def get_rag_service():
    global _rag_service

    if _rag_service is None:
        _rag_service = RagService()

    return _rag_service