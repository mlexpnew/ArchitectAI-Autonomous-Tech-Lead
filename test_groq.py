from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

print("Loaded:", api_key is not None)
print("Starts with:", api_key[:8])

client = Groq(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Hello"}
        ],
    )

    print("SUCCESS!")
    print(response.choices[0].message.content)

except Exception as e:
    print(type(e))
    print(e)