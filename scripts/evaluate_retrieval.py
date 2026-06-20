import json

from legal_rag.retrieval.retriever import retrieve


def main():
    with open("data/eval_sets/golden_qa.json", "r", encoding="utf-8") as f:
        golden_set = json.load(f)

    total = len(golden_set)

    hit_at_3 = 0
    hit_at_5 = 0

    print("=" * 80)
    print("RETRIEVAL EVALUATION")
    print("=" * 80)

    for i, item in enumerate(golden_set, start=1):

        question = item["question"]
        expected_case = item["expected_source_case_id"]

        results3 = retrieve(question, top_k=3)
        results5 = retrieve(question, top_k=5)

        found3 = False
        found5 = False

        retrieved_cases3 = []
        retrieved_cases5 = []

        for meta in results3["metadatas"][0]:
            case_id = meta["case_id"]
            retrieved_cases3.append(case_id)

            if case_id == expected_case:
                found3 = True

        for meta in results5["metadatas"][0]:
            case_id = meta["case_id"]
            retrieved_cases5.append(case_id)

            if case_id == expected_case:
                found5 = True

        if found3:
            hit_at_3 += 1

        if found5:
            hit_at_5 += 1

        print(f"\nQ{i}: {question}")
        print(f"Expected : {expected_case}")
        print(f"Top-3    : {retrieved_cases3}")
        print(f"Top-5    : {retrieved_cases5}")
        print(
            f"Hit@3={'YES' if found3 else 'NO'} | "
            f"Hit@5={'YES' if found5 else 'NO'}"
        )

    print("\n" + "=" * 80)

    recall3 = (hit_at_3 / total) * 100
    recall5 = (hit_at_5 / total) * 100

    print(f"Questions : {total}")
    print(f"Hit@3     : {hit_at_3}/{total}")
    print(f"Hit@5     : {hit_at_5}/{total}")
    print(f"Recall@3  : {recall3:.2f}%")
    print(f"Recall@5  : {recall5:.2f}%")

    print("=" * 80)


if __name__ == "__main__":
    main()