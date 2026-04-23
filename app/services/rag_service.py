import chromadb

from groq import Groq
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class RagService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        self.chroma = chromadb.PersistentClient(path=settings.chroma_path)

        self.collection = self.chroma.get_collection("knowledge_base")

    def ask(self, query: str, top_k: int = 3):
        query_embedding = self.embedder.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        docs = results["documents"][0]
        metas = results["metadatas"][0]

        context = "\n\n".join(docs)

        prompt = f"""
You are a company knowledge assistant.

Use ONLY the provided context to answer the question.
If the answer is not in the context, say you do not know.

Context:
{context}

Question:
{query}
"""

        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": "You answer using only retrieved company documents."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        answer = response.choices[0].message.content

        sources = [
            {
                "source": meta["source"],
                "chunk_id": meta["chunk_id"],
            }
            for meta in metas
        ]

        return {
            "answer": answer,
            "sources": sources
        }


rag_service = RagService()