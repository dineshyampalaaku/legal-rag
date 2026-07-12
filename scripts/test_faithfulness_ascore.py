import asyncio

from google import genai
from ragas.llms import llm_factory
from ragas.metrics.collections.faithfulness import Faithfulness

from legal_rag.configs.settings import settings


# -------------------------------------------------------
# Create Instructor LLM
# -------------------------------------------------------

client = genai.Client(
    api_key=settings.gemini_api_key,
)

llm = llm_factory(
    provider="google",
    model="gemini-2.5-flash-lite",
    client=client,
)


# -------------------------------------------------------
# Create Faithfulness Metric
# -------------------------------------------------------

metric = Faithfulness(
    llm=llm,
)


# -------------------------------------------------------
# Test
# -------------------------------------------------------

async def main():

    result = await metric.ascore(
        user_input="What offence is defined under Section 138 of the Negotiable Instruments Act?",

        response=(
            "Section 138 defines the offence of dishonour of a cheque "
            "due to insufficiency of funds."
        ),

        retrieved_contexts=[
            (
                "Section 138 of the Negotiable Instruments Act "
                "deals with dishonour of cheques for insufficiency "
                "of funds in the account."
            )
        ],
    )

    print("\nReturned object:")
    print(result)

    print("\nType:")
    print(type(result))

    print("\nScore:")
    print(result.value)


if __name__ == "__main__":
    asyncio.run(main())