# tests/unit/test_chroma_store.py
import uuid
import pytest
import chromadb
from langchain_core.documents import Document
from legal_rag.retrieval import chroma_store

@pytest.fixture
def collection(monkeypatch):
    client = chromadb.EphemeralClient()

    collection_name = f"test_{uuid.uuid4().hex}"

    c = client.get_or_create_collection(collection_name)

    monkeypatch.setattr(
        chroma_store,
        "get_collection",
        lambda: c
    )

    return c

def test_upsert_adds_items(collection):
    chunks = [Document(page_content="a", metadata={"chunk_id": "d1_0"}),
              Document(page_content="b", metadata={"chunk_id": "d1_1"})]
    chroma_store.upsert_chunks(chunks, [[0.1, 0.2], [0.3, 0.4]])
    assert collection.count() == 2

def test_upsert_raises_on_length_mismatch(collection):
    chunks = [Document(page_content="a", metadata={"chunk_id": "d1_0"})]
    with pytest.raises(ValueError):
        chroma_store.upsert_chunks(chunks, [[0.1, 0.2], [0.3, 0.4]])

def test_upsert_empty_is_noop(collection):
    chroma_store.upsert_chunks([], [])
    assert collection.count() == 0

def test_upsert_same_chunk_id_overwrites_not_duplicates(collection):
    chroma_store.upsert_chunks(
        [Document(page_content="v1", metadata={"chunk_id": "d1_0"})], [[0.1, 0.2]])
    chroma_store.upsert_chunks(
        [Document(page_content="v2", metadata={"chunk_id": "d1_0"})], [[0.5, 0.6]])
    assert collection.count() == 1

def test_query_returns_top_k(collection):
    chunks = [Document(page_content=f"t{i}", metadata={"chunk_id": f"d1_{i}"}) for i in range(10)]
    chroma_store.upsert_chunks(chunks, [[float(i)] * 2 for i in range(10)])
    res = chroma_store.query([0.0, 0.0], top_k=3)
    assert len(res["ids"][0]) == 3