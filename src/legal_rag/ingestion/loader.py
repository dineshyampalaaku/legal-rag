
"""Load raw legal documents and chunk them with legal-structure awareness."""
from pathlib import Path
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from legal_rag.configs.settings import settings

# Order matters: try to split on legal structure BEFORE generic whitespace.
# Splitting mid-section is one of the failure modes you'll document in RAGAS.
LEGAL_SEPARATORS = [
    "\n\nSection ",
    "\n\nSCHEDULE",
    "\n\nSec. ",
    "\n\n",
    "\n",
    ". ",
    " ",
    "",
]
_LEADING_NOISE = re.compile(
    r"^[\s\.\,\;]+"
)


def load_raw_document(file_path: Path) -> Document:
    """Load a single text document with source metadata attached."""
    if not file_path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    text = file_path.read_text(encoding="utf-8", errors="replace")
    return Document(
        page_content=text,
        metadata={"source": file_path.name, "case_id": file_path.stem},
    )


def chunk_document(doc: Document) -> list[Document]:
    """Split a document into chunks using config-driven size/overlap."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=LEGAL_SEPARATORS,
    )
    chunks = splitter.split_documents([doc])
    chunks = [c for c in chunks if c.page_content.strip()]

    # Tag each chunk with its index — needed later to debug
    # "retrieved chunk lost context from neighbor" failure mode.
    for i, chunk in enumerate(chunks):
      chunk.page_content = (
        _LEADING_NOISE.sub(
            "",
            chunk.page_content
        ).strip()
      )

      chunk.metadata["chunk_id"] = (
        f"{chunk.metadata['case_id']}_chunk_{i}"
      )

      chunk.metadata["chunk_index"] = i
      chunk.metadata["total_chunks"] = len(chunks)

    return chunks


def load_and_chunk_directory(raw_dir: Path = Path("data/raw")) -> list[Document]:
    """Process all .txt files in raw_dir into chunked documents."""
    all_chunks = []
    for file_path in sorted(raw_dir.glob("*.txt")):
        doc = load_raw_document(file_path)
        all_chunks.extend(chunk_document(doc))
    return all_chunks