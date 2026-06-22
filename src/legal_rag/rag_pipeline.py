from legal_rag.retrieval.retriever import retrieve
from legal_rag.generation.generator import generate_answer


def ask(question: str, top_k: int = 3) -> dict:
    results = retrieve(question, top_k=top_k)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(documents)

    answer = generate_answer(
        question=question,
        context=context
    )

    sources = []

    for meta in metadatas:
        sources.append(
            {
                "case_id": meta["case_id"],
                "chunk_id": meta["chunk_id"],
                "source_file": meta["source"]
            }
        )

    return {
        "answer": answer,
        "sources": sources
    }