from unittest.mock import patch

from legal_rag.rag_pipeline import ask


@patch("legal_rag.rag_pipeline.generate_answer")
@patch("legal_rag.rag_pipeline.retrieve")
def test_ask_returns_generated_answer(
    mock_retrieve,
    mock_generate
):
    mock_retrieve.return_value = {
        "documents": [["chunk1", "chunk2"]]
    }

    mock_generate.return_value = "Final Answer"

    result = ask("test question")

    assert result == "Final Answer"