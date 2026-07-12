from google import genai

from ragas.llms import llm_factory
from ragas.metrics.collections.faithfulness import Faithfulness

from legal_rag.configs.settings import settings


client = genai.Client(
    api_key=settings.gemini_api_key,
)

llm = llm_factory(
    model="gemini-2.5-flash-lite",
    provider="google",
    client=client,
)

metric = Faithfulness(
    llm=llm,
)

print(type(metric))
print(metric)