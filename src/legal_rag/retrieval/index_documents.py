from legal_rag.ingestion.loader import load_and_chunk_directory
from legal_rag.embeddings.embedder import embed_texts
from legal_rag.retrieval.chroma_store import upsert_chunks


def main():
    print("Loading documents...")

    chunks = load_and_chunk_directory()

    print(f"Loaded {len(chunks)} chunks")

    print("Generating embeddings and storing in ChromaDB...")

    BATCH_SIZE = 20

    for i in range(0, len(chunks), BATCH_SIZE):
        batch_chunks = chunks[i:i + BATCH_SIZE]

        batch_texts = [
            c.page_content
            for c in batch_chunks
        ]

        print(
            f"Processing batch {i // BATCH_SIZE + 1}"
            f" / {(len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE}"
        )

        vectors = embed_texts(batch_texts)

        upsert_chunks(
            batch_chunks,
            vectors
        )

    print("Done!")
    print(f"Indexed {len(chunks)} chunks")


if __name__ == "__main__":
    main()