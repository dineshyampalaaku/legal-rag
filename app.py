import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.title("⚖️ Legal RAG Assistant")

question = st.text_input(
    "Ask a legal question"
)

if st.button("Ask"):

    if question:

        response = requests.post(
            API_URL,
            json={"question": question}
        )

        data = response.json()

        st.subheader("Answer")
        st.write(data["answer"])

        st.subheader("Sources")

        for source in data["sources"]:
            st.write(
                f"{source['case_id']} | "
                f"{source['chunk_id']}"
            )