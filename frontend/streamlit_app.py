import requests
import streamlit as st

import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/ask"
)

st.set_page_config(
    page_title="LexInsight AI",
    page_icon="⚖️",
    layout="wide",
)

# ---------- HEADER ----------

st.title("⚖️ LexInsight AI")

st.caption(
    "AI-powered Legal Research Assistant using Retrieval-Augmented Generation (RAG)"
)

st.markdown("---")

# ---------- PROJECT STATS ----------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Legal Cases", "5")

with col2:
    st.metric("Knowledge Chunks", "387")

with col3:
    st.metric("LLM", "Gemini 2.5 Flash")

st.markdown("---")

# ---------- QUESTION ----------

st.subheader("Ask a Legal Question")

question = st.text_area(
    "Legal Question",
    placeholder="Example: What offence is defined under Section 138 of the Negotiable Instruments Act?",
    label_visibility="collapsed",
    height=140,
)

ask = st.button("🔍 Analyze Question", use_container_width=True)

if ask:

    if question.strip() == "":
        st.warning("Please enter a legal question.")
        st.stop()

    with st.spinner("Searching relevant judgments..."):

        response = requests.post(
            API_URL,
            json={"question": question},
            timeout=120,
        )

    if response.status_code != 200:
        st.error("Backend request failed.")
        st.stop()

    result = response.json()

    st.markdown("---")

    st.subheader("📖 AI Analysis")

    st.success(result["answer"])

    st.markdown("---")

    st.subheader("📚 Supporting Evidence")

    for source in result["sources"]:

        with st.container(border=True):

            c1, c2 = st.columns([3,2])

            with c1:
                st.markdown(f"**Case**")
                st.write(source["case_id"])

                st.markdown("**Source File**")
                st.write(source["source_file"])

            with c2:
                st.markdown("**Chunk ID**")
                st.code(source["chunk_id"])

st.markdown("---")

st.caption(
    "LexInsight AI • FastAPI • Gemini • ChromaDB • Streamlit"
)