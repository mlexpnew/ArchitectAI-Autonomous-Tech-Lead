from crewai import LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

response = llm.call("Say hello in one sentence.")

print(response)