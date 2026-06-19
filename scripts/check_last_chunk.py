from legal_rag.retrieval.chroma_store import get_collection

collection = get_collection()

data = collection.get()

print("Total:", len(data["ids"]))

for chunk_id in data["ids"][-20:]:
    print(chunk_id)