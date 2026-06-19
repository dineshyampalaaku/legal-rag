from legal_rag.embeddings.embedder import embed_texts
from legal_rag.retrieval.chroma_store import query


def retrieve(query_text: str, top_k: int = 5):
    """
    Retrieve top-k relevant chunks for a query.
    """

    query_embedding = embed_texts([query_text])[0]

    results = query(
        query_embedding=query_embedding,
        top_k=top_k
    )

    return results