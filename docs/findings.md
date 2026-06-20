# Legal RAG Findings

## Corpus

- 5 Supreme Court Judgments
- 387 Chunks Indexed

## Retrieval Metrics

- Recall@3 = 90%
- Recall@5 = 95%

## Failure Case #1

Question:

What issue relating to company liability is discussed in Hiten Dalal?

Expected:

Operation of statutory presumptions and evidentiary burden.

Retrieved:

- hiten_dalal_chunk_0
- hiten_dalal_chunk_4

Observation:

Retriever correctly returned Hiten Dalal chunks.

However, the retrieved context emphasized Section 141
(Offences by Companies).

The question wording caused ambiguity.

Conclusion:

Not a pure retrieval failure.
Potential question-design issue.