from config.llm import llm

response = llm.call("Say hello in one sentence.")

print(response)