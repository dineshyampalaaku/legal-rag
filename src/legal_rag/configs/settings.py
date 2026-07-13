from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # LLM
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    gemini_model: str = "gemini-1.5-pro"

    # Embeddings
    embedding_model: str = "models/gemini-embedding-001"
    embedding_batch_size: int = 5
    embedding_dimension: int = 3072

    # ChromaDB
    chroma_persist_dir: str = "./data/chroma"
    collection_name: str = "indian_legal_docs"

    # Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Retrieval
    retrieval_top_k: int = 5

    # Observability
    langsmith_api_key: str | None = Field(default=None, env="LANGSMITH_API_KEY")
    langsmith_project: str = "legal-rag-prod"

    # Eval
    ragas_sample_size: int = 50

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

import os

#os.environ["LANGSMITH_TRACING"] = "true"
#os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
#os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project