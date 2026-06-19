from unittest.mock import patch

from legal_rag.generation.generator import generate_answer


@patch("legal_rag.generation.generator.client")
def test_generate_answer_returns_text(mock_client):

    mock_client.models.generate_content.return_value.text = (
        "Section 138 deals with cheque dishonour."
    )

    answer = generate_answer(
        "What is Section 138?",
        "Section 138 deals with cheque dishonour."
    )

    assert "Section 138" in answer