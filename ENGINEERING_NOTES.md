# Engineering Notes

This document captures the engineering decisions, debugging process, evaluation observations, deployment challenges, and lessons learned while building the **Legal Document Intelligence System**.

Unlike the README, which describes the final system, this document focuses on **how the system evolved during development**.

---

# Project Objective

The initial goal was to build an end-to-end Retrieval-Augmented Generation (RAG) system capable of answering questions from legal judgments using semantic retrieval and Large Language Models.

The project emphasized:

- Modular architecture
- Retrieval quality
- Grounded answer generation
- Evaluation using RAGAS
- Production deployment

rather than simply building a chatbot interface.

---

# Major Engineering Decisions

## 1. FastAPI Backend

The backend was separated from the frontend to expose the RAG pipeline through REST APIs.

Benefits:

- reusable backend
- independent frontend
- production deployment
- easier testing

---

## 2. Streamlit Frontend

Instead of spending significant effort on frontend development, Streamlit was chosen to rapidly demonstrate the AI pipeline.

The objective of Version 1 was validating the RAG system rather than building a production UI.

---

## 3. ChromaDB

ChromaDB was selected because it offers:

- lightweight deployment
- persistent vector storage
- semantic similarity search
- straightforward Python integration

For the current project size, it was sufficient without introducing additional infrastructure.

---

## 4. Google Gemini

Gemini was used for both:

- Embedding generation
- Answer generation

Using the same provider simplified API integration and maintained consistency across the retrieval pipeline.

---

## 5. RAGAS

Evaluation was incorporated from the beginning rather than relying solely on manual inspection.

This helped verify that generated responses remained grounded in the retrieved legal judgments.

---

# Engineering Challenges

## Challenge 1 — Project Structure

The project evolved from a simple prototype into a modular architecture.

The codebase was reorganized into independent modules for:

- ingestion
- embeddings
- retrieval
- generation
- evaluation
- API
- configuration

This improved maintainability and separation of concerns.

---

## Challenge 2 — Dependency Management

During development, multiple Python environments were used:

- development
- evaluation
- RAGAS

Dependency conflicts between LangChain, RAGAS, ChromaDB, and Gemini libraries required careful environment isolation.

---

## Challenge 3 — RAGAS Integration

Integrating RAGAS required multiple iterations.

Challenges included:

- dataset formatting
- metric compatibility
- API changes
- evaluation pipeline debugging

Smoke-test evaluation was ultimately achieved using representative legal questions.

---

## Challenge 4 — LangSmith

LangSmith integration was explored for tracing and observability.

However, API configuration and compatibility issues prevented successful integration within the project timeline.

Rather than blocking deployment, tracing was made optional so the core RAG system remained functional.

This highlighted the importance of separating optional observability tooling from core application functionality.

---

## Challenge 5 — Deployment

Deploying locally working code required additional engineering work.

Major deployment tasks included:

- Render backend configuration
- Streamlit Cloud deployment
- environment variable management
- packaging dependencies
- ChromaDB persistence
- startup configuration

The deployed system now exposes:

- REST API
- Swagger documentation
- Streamlit frontend

---

# Evaluation Observations

The project was evaluated using RAGAS smoke tests.

Representative metrics included:

| Metric | Result |
|---------|--------|
| Faithfulness | 1.00 |
| Context Recall | 1.00 |
| Answer Relevancy | 0.92 |

The evaluation demonstrated that generated answers remained grounded within the retrieved legal context.

---

# Current Limitations

The current version intentionally focuses on validating the RAG pipeline.

Known limitations include:

- curated legal corpus
- static vector database
- no runtime PDF upload
- no dynamic indexing
- no authentication
- no conversation memory

These limitations are planned improvements rather than architectural constraints.

---

# Lessons Learned

This project provided practical experience with:

- Retrieval-Augmented Generation
- vector databases
- semantic search
- prompt grounding
- evaluation using RAGAS
- REST API development
- deployment
- debugging dependency conflicts
- production configuration

One of the biggest lessons was that building an AI application involves considerably more engineering than simply calling an LLM API.

Reliable retrieval, evaluation, deployment, and maintainability are equally important.

---

# Future Improvements

Version 2 is planned to include:

- runtime PDF upload
- automatic document ingestion
- dynamic vector indexing
- multi-document retrieval
- improved UI
- hybrid retrieval
- reranking
- larger legal corpus

These improvements will extend the current engineering foundation without requiring major architectural changes.