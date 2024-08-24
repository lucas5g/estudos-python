from langchain_groq import ChatGroq 
from langchain_openai import ChatOpenAI

import os


print(os.getenv("GROQ_API_KEY"))
def find_model(model:str):
    model = model.lower()
    
    if model == 'llama3-8b-8192' or model == 'llama-3.1-8b-instant':
        return ChatGroq(
            model=model,
            temperature=0,
            api_key=os.getenv('GROQ_API_KEY')
        )

    if model == 'gpt-3.5-turbo' or model == 'gpt-4o':
        return ChatOpenAI(
            model=model,
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )        
    return 'Modelo não cadastrado :('

models = [
    "LLAMA-3.1-8B-INSTANT",
    "LLAMA3-8B-8192",
    "GPT-3.5-TURBO",
    "GPT-4o",    
]


