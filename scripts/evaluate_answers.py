import json
import csv
import time

from legal_rag.retrieval.retriever import retrieve
from legal_rag.generation.generator import generate_answer

def main():
    with open("data/eval_sets/golden_qa.json", "r", encoding="utf-8") as f:
        golden_set = json.load(f)

    rows = []

    print("=" * 80)
    print("ANSWER EVALUATION")
    print("=" * 80)

    for i, item in enumerate(golden_set, start=1):

        question = item["question"]
        ground_truth = item["ground_truth"]

        print(f"\n[{i}/{len(golden_set)}] {question}")

        try:
          retrieval_result = retrieve(question, top_k=5)

          chunk_ids = retrieval_result["ids"][0]

          context = "\n\n".join(
            retrieval_result["documents"][0]
          )

          answer = generate_answer(
            question=question,
            context=context
          )

          time.sleep(15)

        except Exception as e:
          answer = f"ERROR: {e}"
          chunk_ids = []

        rows.append(
            {
                "question": question,
                "ground_truth": ground_truth,
                "retrieved_chunk_ids": ";".join(chunk_ids),
                "generated_answer": answer,
            }
        )

    with open(
        "data/eval_sets/answer_evaluation.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "question",
                "ground_truth",
                "retrieved_chunk_ids",
                "generated_answer",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    print("\nDone!")
    print("Saved: data/eval_sets/answer_evaluation.csv")


if __name__ == "__main__":
    main()