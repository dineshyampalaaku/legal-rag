from legal_rag.retrieval.retriever import retrieve
from legal_rag.generation.generator import generate_answer


def ask(question: str, top_k: int = 3) -> str:
    results = retrieve(question, top_k=top_k)

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    answer = generate_answer(
        question=question,
        context=context
    )

    return answer