# src/legal_rag/embeddings/embedder.py
"""Gemini embeddings: batched, retried on transient errors, traced to LangSmith."""
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, DeadlineExceeded
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langsmith import traceable
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from legal_rag.configs.settings import settings

_embedder = None
def get_embedder():
    global _embedder

    if _embedder is None:
        _embedder = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.gemini_api_key
        )

    return _embedder
_TRANSIENT = (ResourceExhausted, ServiceUnavailable, DeadlineExceeded)


@retry(wait=wait_exponential(multiplier=2, min=2, max=60),
       stop=stop_after_attempt(5),
       retry=retry_if_exception_type(_TRANSIENT))
def _embed_batch(texts: list[str]) -> list[list[float]]:
    vectors = get_embedder().embed_documents(texts)

    if len(vectors) != len(texts):
        raise ValueError(
            f"Embedding count mismatch: {len(vectors)} vectors for {len(texts)} texts"
        )

    if vectors and len(vectors[0]) != settings.embedding_dimension:
        raise ValueError(
            f"Expected {settings.embedding_dimension}-dim, got {len(vectors[0])}"
        )

    return vectors


@traceable(name="embed_texts")
def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    batch_size = settings.embedding_batch_size
    vectors: list[list[float]] = []
    for i in range(0, len(texts), batch_size):
        vectors.extend(_embed_batch(texts[i : i + batch_size]))
    return vectors