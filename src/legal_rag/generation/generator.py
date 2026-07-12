import time
from langsmith import traceable
from google import genai

from legal_rag.configs.settings import settings


client = genai.Client(
    api_key=settings.gemini_api_key
)


@traceable(name="generate_answer")
def generate_answer(
    question: str,
    context: str
) -> str:

    prompt = f"""
You are a legal assistant.

Use ONLY the context provided below to answer the user's question.

If the context contains the answer:
- Give a clear legal answer.
- Do not make up information.

If the answer is not found in the context:
Respond exactly with:

I could not find the answer in the provided documents.

Context:
{context}

Question:
{question}

Answer:
"""

    for attempt in range(3):

     try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        return response.text

     except Exception as e:

        print(f"[Generator] Attempt {attempt + 1}/3 failed.")

        print(e)

        if attempt < 2:

            wait_time = 2 ** attempt

            print(f"[Generator] Retrying in {wait_time} seconds...")

            time.sleep(wait_time)

        else:

            return f"Model temporarily unavailable: {str(e)}"