from pathlib import Path
from legal_rag.ingestion.loader import load_and_chunk_directory

chunks = load_and_chunk_directory(Path("data/raw"))

print(f"Total Chunks: {len(chunks)}")

for i in [20, 40, 60, 80, 100]:
    print("\n" + "=" * 80)
    print(f"CHUNK {i}")
    print(chunks[i].metadata)
    print()
    print(chunks[i].page_content[:1000])