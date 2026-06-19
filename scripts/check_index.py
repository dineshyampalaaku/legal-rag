from legal_rag.retrieval.chroma_store import get_collection

collection = get_collection()

print("Count:", collection.count())

sample = collection.get(limit=5)

print(sample["ids"])