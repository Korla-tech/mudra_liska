import openai
import json

with open("key.json") as f:
    openai.api_key = json.load(f)["openaikey"]


def generate(prompt):
    response = openai.Completion.create(
        engine="text-curie-001", prompt=str(prompt), temperature=0.7, max_tokens=256)

    return response["choices"][0]["text"]
