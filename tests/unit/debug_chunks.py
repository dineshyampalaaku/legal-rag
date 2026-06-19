from pathlib import Path

from legal_rag.ingestion.loader import load_and_chunk_directory

chunks = load_and_chunk_directory(Path("data/raw"))

print(f"Actual chunk count: {len(chunks)}")

print("\nFIRST CHUNK:")
print(chunks[0].metadata)

print("\nLAST CHUNK:")
print(chunks[-1].metadata)