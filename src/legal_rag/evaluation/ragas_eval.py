import json
import time
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from legal_rag.configs.settings import settings
from datasets import Dataset

llm = LangchainLLMWrapper(
    ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=settings.gemini_api_key,
    )
)

embeddings = LangchainEmbeddingsWrapper(
    GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=settings.gemini_api_key,
    )
)
from ragas import evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
    faithfulness,
    answer_relevancy,
)

from legal_rag.retrieval.retriever import retrieve
from legal_rag.generation.generator import generate_answer


def build_dataset():

    with open(
        "data/eval_sets/golden_qa.json",
        "r",
        encoding="utf-8"
    ) as f:
        golden_set = json.load(f)

    rows = []

    for item in golden_set[:1]:

        question = item["question"]
        ground_truth = item["ground_truth"]

        retrieval_result = retrieve(
            question,
            top_k=5
        )

        contexts = retrieval_result["documents"][0]

        context_text = "\n\n".join(contexts)

        answer = generate_answer(
            question=question,
            context=context_text
        )

        rows.append(
            {
                "question": question,
                "answer": answer,
                "contexts": contexts,
                "ground_truth": ground_truth,
            }
        )

        time.sleep(15)

    return Dataset.from_list(rows)


def main():

    dataset = build_dataset()

    print("\nCOLUMN NAMES:")
    print(dataset.column_names)

    print("\nFIRST ROW:")
    print(dataset[0])

    return

    result = evaluate(
       dataset=dataset,
       metrics=[
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
      ],
      llm=llm,
      embeddings=embeddings,
    )

    print(result)


if __name__ == "__main__":
    main()