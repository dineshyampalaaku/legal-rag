# tests/unit/test_embedder.py
import pytest
from unittest.mock import patch
from google.api_core.exceptions import ResourceExhausted
from legal_rag.embeddings.embedder import embed_texts

def test_embed_texts_empty_returns_empty():
    assert embed_texts([]) == []

@patch("legal_rag.embeddings.embedder._embedder")
def test_embed_texts_returns_vector_per_input(mock_embedder):
    vectors = [
        [0.1] * 3072,
        [0.2] * 3072,
    ]
    mock_embedder.embed_documents.return_value = vectors
    assert embed_texts(["a", "b"]) == vectors

@patch("legal_rag.embeddings.embedder._embedder")
def test_embed_texts_raises_on_count_mismatch(mock_embedder):
    mock_embedder.embed_documents.return_value = [[0.1, 0.2]]  # 1 vector for 2 inputs
    with pytest.raises(ValueError):
        embed_texts(["a", "b"])

@patch("legal_rag.embeddings.embedder._embedder")
def test_embed_texts_retries_on_rate_limit(mock_embedder):
    vectors = [[0.1] * 3072]
    mock_embedder.embed_documents.side_effect = [
        ResourceExhausted("429"),
        vectors
    ]
    assert embed_texts(["a"]) == vectors
    
@patch("legal_rag.embeddings.embedder.get_embedder")
def test_embed_texts_raises_on_wrong_dimension(mock_get_embedder):
    mock_embedder = mock_get_embedder.return_value

    mock_embedder.embed_documents.return_value = [
        [0.1] * 768
    ]

    with pytest.raises(ValueError):
        embed_texts(["test"])