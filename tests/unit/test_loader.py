from pathlib import Path

from legal_rag.ingestion.loader import load_and_chunk_directory


def test_chunking_produces_multiple_chunks():
    chunks = load_and_chunk_directory(Path("data/raw"))

    assert len(chunks) > 1

    assert all(
        "chunk_index" in c.metadata
        for c in chunks
    )

    assert all(
        "total_chunks" in c.metadata
        for c in chunks
    )

    from collections import defaultdict

    per_doc_counts = defaultdict(int)

    for chunk in chunks:
     per_doc_counts[chunk.metadata["source"]] += 1

    for chunk in chunks:
        source = chunk.metadata["source"]

        assert (
          chunk.metadata["total_chunks"]
          == per_doc_counts[source]
        )
    
    
def test_empty_directory_returns_empty_list(tmp_path):
    assert load_and_chunk_directory(tmp_path) == []


def test_non_txt_files_ignored(tmp_path):
    (tmp_path / "ignore.pdf").write_bytes(
        b"%PDF-1.4 fake"
    )

    (tmp_path / "case.txt").write_text(
        "Section 1. Text.",
        encoding="utf-8"
    )

    chunks = load_and_chunk_directory(tmp_path)

    assert all(
        c.metadata["source"] == "case.txt"
        for c in chunks
    )   
    
def test_chunks_have_no_leading_punctuation_noise():
    chunks = load_and_chunk_directory(
        Path("data/raw")
    )

    for chunk in chunks:
        assert not chunk.page_content.startswith(
            (".", " ", "\n")
        )