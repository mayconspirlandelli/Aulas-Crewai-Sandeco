from pydantic import BaseModel
from dotenv import load_dotenv
import os
from crewai import LLM

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()  # Isso carrega as variáveis do .env para os.environ

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class Dog(BaseModel):
    name: str
    age: int
    breed: str


# llm = LLM(model="gpt-4o", response_format=Dog)
llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=GOOGLE_API_KEY,
    response_format=Dog,
)


response = llm.call(
    "Analyze the following messages and return the name, age, and breed. "
    "Meet Kona! She is 3 years old and is a black german shepherd."
)
print(response)

# Output:
# Dog(name='Kona', age=3, breed='black german shepherd')