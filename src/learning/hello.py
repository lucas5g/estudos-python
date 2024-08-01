LANGCHAIN_TRACING_V2=True
# LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="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"
LANGCHAIN_PROJECT="pr-scholarly-visitor-39"
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
llm.invoke("Hello, world!")