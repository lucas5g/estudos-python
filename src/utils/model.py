from dotenv import load_dotenv 
from langchain_openai import ChatOpenAI 
from langchain_groq import ChatGroq

load_dotenv() 

model = ChatOpenAI(model='gpt-3.5-turbo')

llm_groq = ChatGroq(
    temperature=0,
    model='llama3-8b-8192'
)