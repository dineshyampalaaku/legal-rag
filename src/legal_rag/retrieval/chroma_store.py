# src/legal_rag/retrieval/chroma_store.py
"""ChromaDB persistence layer — upsert and query chunk embeddings."""
import chromadb
from langsmith import traceable
from legal_rag.configs.settings import settings


def get_collection():
    client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    return client.get_or_create_collection(name=settings.collection_name)


def upsert_chunks(chunks, embeddings: list[list[float]]) -> None:
    if len(chunks) != len(embeddings):
        raise ValueError(f"Mismatch: {len(chunks)} chunks vs {len(embeddings)} embeddings")
    if not chunks:
        return
    get_collection().upsert(
        ids=[c.metadata["chunk_id"] for c in chunks],
        embeddings=embeddings,
        documents=[c.page_content for c in chunks],
        metadatas=[c.metadata for c in chunks],
    )


@traceable(name="chroma_query")
def query(query_embedding: list[float], top_k: int | None = None) -> dict:
    return get_collection().query(
        query_embeddings=[query_embedding],
        n_results=top_k or settings.retrieval_top_k,
    )