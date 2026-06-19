from unittest.mock import patch

from legal_rag.retrieval.retriever import retrieve


@patch("legal_rag.retrieval.retriever.query")
@patch("legal_rag.retrieval.retriever.embed_texts")
def test_retrieve_returns_results(
    mock_embed,
    mock_query
):
    mock_embed.return_value = [[0.1, 0.2]]

    mock_query.return_value = {
        "ids": [["c1", "c2"]]
    }

    result = retrieve(
        "section 138",
        top_k=2
    )

    assert result["ids"][0] == ["c1", "c2"]

    mock_embed.assert_called_once()
    mock_query.assert_called_once()