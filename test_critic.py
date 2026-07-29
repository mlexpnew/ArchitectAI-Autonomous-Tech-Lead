from quality.critic_agent import CriticAgent

code = """
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"hello":"world"}
"""

report = CriticAgent().review(code)

print()

print("=" * 60)

print(report)