from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCS_PATH = Path("docs")
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "knowledge_base"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

documents = list(DOCS_PATH.glob("*.md"))

ids = []
texts = []
metadatas = []

counter = 0

for file in documents:
    content = file.read_text(encoding="utf-8")
    chunks = splitter.split_text(content)

    for idx, chunk in enumerate(chunks):
        ids.append(f"doc-{counter}")
        texts.append(chunk)
        metadatas.append(
            {
                "source": file.name,
                "chunk_id": idx,
            }
        )
        counter += 1

embeddings = model.encode(texts).tolist()

collection.upsert(
    ids=ids,
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas
)

print(f"Indexed {len(texts)} chunks successfully.")