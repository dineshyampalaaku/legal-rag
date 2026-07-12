# scripts/ragas_eval.py
import asyncio
import csv
import json
import subprocess
from datetime import datetime
from pathlib import Path
import traceback

from google import genai
from ragas.llms import llm_factory
from ragas.metrics.collections.faithfulness.metric import Faithfulness
from ragas.metrics.collections.context_recall.metric import ContextRecall
from ragas.metrics.collections.context_precision.metric import ContextPrecision
from ragas.metrics.collections import AnswerRelevancy
from ragas.embeddings.google_provider import GoogleEmbeddings


import sys
sys.path.insert(0, "src")
from legal_rag.configs.settings import settings

# ----------------------------------------
# Available Gemini models (priority order)
# ----------------------------------------

MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
]


def create_llm(model_name: str):

    client = genai.Client(
        api_key=settings.gemini_api_key,
    )

    llm = llm_factory(
        provider="google",
        model=model_name,
        client=client,
    )

    embeddings = GoogleEmbeddings(
        client=client,
        model="gemini-embedding-001",
    )

    return llm, embeddings

async def run_metric(metric_class, metric_name, score_kwargs):

    last_exception = None

    for model_name in MODELS:

        print(f"\nTrying {metric_name} using {model_name}")

        llm, embeddings = create_llm(model_name)

        if metric_class is AnswerRelevancy:
            metric = metric_class(
                llm=llm,
                embeddings=embeddings,
            )
        else:
            metric = metric_class(
                llm=llm,
            )

        for attempt in range(3):

            try:

                result = await metric.ascore(**score_kwargs)

                print(
                    f"{metric_name} succeeded using {model_name}"
                )

                return float(result.value)

            except Exception as e:

                last_exception = e

                print(
                    f"{metric_name} failed "
                    f"(Model={model_name}, Attempt={attempt+1})"
                )

                print(e)

                if "503" not in str(e):
                    break

                wait_time = (attempt + 1) * 10

                print(
                    f"Waiting {wait_time} seconds before retry..."
                )

                await asyncio.sleep(wait_time)

    raise last_exception


async def score_one(item: dict) -> dict:
    user_input         = item["user_input"]
    reference          = item["reference"]
    retrieved_contexts = item["retrieved_contexts"]
    response           = item["response"]

    scores = {"question": user_input}
    #faithfulness: (user_input, response, retrieved_contexts)
    try:

        scores["faithfulness"] = await run_metric(
            metric_class=Faithfulness,
            metric_name="Faithfulness",
            score_kwargs={
                "user_input": user_input,
                "response": response,
                "retrieved_contexts": retrieved_contexts,
            },
        )

    except Exception as e:

        traceback.print_exc()

        print(f"Faithfulness error: {e}")

        scores["faithfulness"] = None

    # ContextRecall: (user_input, retrieved_contexts, reference)
    try:

        scores["context_recall"] = await run_metric(
            metric_class=ContextRecall,
            metric_name="ContextRecall",
            score_kwargs={
                "user_input": user_input,
                "retrieved_contexts": retrieved_contexts,
                "reference": reference,
            },
        )

    except Exception as e:

        traceback.print_exc()

        print(f"ContextRecall error: {e}")

        scores["context_recall"] = None

    # ContextPrecision: (user_input, reference, retrieved_contexts)
    try:

        scores["context_precision"] = await run_metric(
            metric_class=ContextPrecision,
            metric_name="ContextPrecision",
            score_kwargs={
                "user_input": user_input,
                "reference": reference,
                "retrieved_contexts": retrieved_contexts,
            },
        )

    except Exception as e:

        traceback.print_exc()

        print(f"ContextPrecision error: {e}")

        scores["context_precision"] = None


    # AnswerRelevancy: (user_input, response)
    try:

        scores["answer_relevancy"] = await run_metric(
            metric_class=AnswerRelevancy,
            metric_name="AnswerRelevancy",
            score_kwargs={
                "user_input": user_input,
                "response": response,
            },
        )


    except Exception as e:

        traceback.print_exc()

        print(f"AnswerRelevancy error: {e}")

        scores["answer_relevancy"] = None

    return scores


def main():
    data_path = Path("data/eval_sets/golden_qa_with_answers.json")
    if not data_path.exists():
        print(f"ERROR: {data_path} not found. Run generate_eval_inputs.py first.")
        return

    data = json.loads(
        data_path.read_text(encoding="utf-8")
    )
    samples = data[:3]  # 1 or 5 questions = quota-safe on free tier

    sha = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
    ).decode().strip()

    out_path     = Path("data/eval_sets/ragas_scores.csv")
    history_path = Path("data/eval_sets/eval_history.jsonl")

    fieldnames = [
        "question", "context_precision", "context_recall",
        "faithfulness", "answer_relevancy", "git_sha", "timestamp",
    ]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, item in enumerate(samples):
            print(f"\n[{i+1}/{len(samples)}] {item['user_input'][:70]}")
            try:
                scores = asyncio.run(score_one(item))
            except Exception as e:
                if "RESOURCE_EXHAUSTED" in str(e):
                    print("\nGemini daily quota exhausted.")
                    print("Stopping evaluation.")
                    break
                raise
            scores["git_sha"]   = sha
            scores["timestamp"] = datetime.utcnow().isoformat()

            writer.writerow({k: scores.get(k) for k in fieldnames})
            f.flush()

            with open(history_path, "a", encoding="utf-8") as h:
                h.write(json.dumps(scores) + "\n")

            for k in ["context_precision", "context_recall", "faithfulness", "answer_relevancy"]:
                v = scores.get(k)
                print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    print(f"\nDone. Scores -> {out_path}")


if __name__ == "__main__":
    main()