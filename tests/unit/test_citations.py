from legal_rag.rag_pipeline import ask


def test_ask_returns_sources():
    result = ask(
        "What is Section 138 of the Negotiable Instruments Act?"
    )

    assert "answer" in result
    assert "sources" in result