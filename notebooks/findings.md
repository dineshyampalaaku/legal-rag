# Ingestion Findings

## Finding 001

Document:
Dashrath Rupsingh Rathod vs State Of Maharashtra (SC, 2014)

Result:
155 chunks generated.

Observation:
Many chunks begin with "."

Example:

". As already noted above..."

Cause:
RecursiveCharacterTextSplitter falls back to sentence-level splitting and preserves ". " separator at the beginning of the next chunk.

Impact:
Retrieval quality may degrade slightly because chunks begin with punctuation artifacts.

Status:
Pending cleanup step before embeddings.

## LangSmith Issue

Gemini embedding pipeline validated.

LangSmith authentication remains unresolved.

Verified:

- Multiple Personal Access Tokens created
- Workspace 1 selected
- Key loads from .env
- Key visible in os.environ
- Client() initializes successfully
- Authentication fails even when bypassing project code

Impact:
- Tracing unavailable temporarily

Mitigation:
- Continue development without tracing
- Re-enable once LangSmith account issue is resolved