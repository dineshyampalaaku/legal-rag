import json
import os
import time
from pathlib import Path

from datasets import Dataset

# Force RAGAS to run sequentially
os.environ["RAGAS_MAX_WORKERS"] = "1"

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

from ragas import evaluate
from google import genai
from ragas.llms import llm_factory
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.metrics.collections.faithfulness import Faithfulness

from legal_rag.configs.settings import settings
from legal_rag.retrieval.retriever import retrieve
from legal_rag.generation.generator import generate_answer


# -----------------------------
# LLM
# -----------------------------
client = genai.Client(
    api_key=settings.gemini_api_key,
)

llm = llm_factory(
    model="gemini-2.5-flash-lite",
    provider="google",
    client=client,
)

# -----------------------------
# Embeddings
# -----------------------------
embeddings = LangchainEmbeddingsWrapper(
    GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=settings.gemini_api_key,
    )
)


def build_dataset(num_questions=1):
    """
    Build a RAGAS dataset.
    """

    with open(
        "data/eval_sets/golden_qa.json",
        "r",
        encoding="utf-8",
    ) as f:
        golden_set = json.load(f)

    rows = []

    for item in golden_set[:num_questions]:

        question = item["question"]
        ground_truth = item["ground_truth"]

        retrieval_result = retrieve(
            query_text=question,
            top_k=5,
        )

        contexts = retrieval_result["documents"][0]

        context_text = "\n\n".join(contexts)

        print("\nGenerating answer for:")
        print(question)

        answer = generate_answer(
            question=question,
            context=context_text,
        )

        rows.append(
            {
                "question": question,
                "answer": answer,
                "contexts": contexts,
                "ground_truth": ground_truth,
            }
        )

        # Small delay between requests
        time.sleep(5)

    return Dataset.from_list(rows)


def evaluate_metric(
    dataset,
    metric,
    metric_name,
):
    """
    Run one RAGAS metric.
    """

    print("\n" + "=" * 70)
    print(f"Running {metric_name}")
    print("=" * 70)

    start_time = time.time()

    try:

        result = evaluate(
            dataset=dataset,
            metrics=[metric],
            llm=llm,
            embeddings=embeddings,
        )

        elapsed = time.time() - start_time

        print("\nEvaluation completed successfully.")
        print(f"Time Taken : {elapsed:.2f} seconds")

        print("\nRaw Result:")
        print(result)

        df = result.to_pandas()

        print("\nDataFrame:")
        print(df)

        result_file = Path(
            f"data/eval_sets/{metric_name}.csv"
        )

        df.to_csv(
            result_file,
            index=False,
        )

        print(f"\nResults saved to:\n{result_file}")

        return df

    except Exception as e:

        elapsed = time.time() - start_time

        print("\nEvaluation Failed")
        print(f"Time Taken : {elapsed:.2f} seconds")
        print(e)

        return None


def main():

    dataset = build_dataset(
        num_questions=1,
    )

    print("\nDataset Created Successfully")
    print(dataset)

    evaluate_metric(
        dataset=dataset,
        metric=Faithfulness(
            llm=llm,
        ),
        metric_name="faithfulness",
    )


if __name__ == "__main__":
    main()