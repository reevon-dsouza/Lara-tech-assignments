import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "https://agentic-training2026.services.ai.azure.com/openai/v1")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

client = OpenAI(
    base_url=endpoint,
    api_key=api_key,
)

SYSTEM_PROMPT = "You are a friendly and helpful chatbot. Keep responses concise."


def chat():
    print("Simple chatbot ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Chatbot: Goodbye!")
            break

        if not user_input:
            print("Chatbot: Please enter a message.\n")
            continue

        try:
            response = client.responses.create(
                model=deployment_name,
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ],
            )
            print(f"Chatbot: {response.output_text}\n")
        except Exception as exc:
            print(f"Chatbot: Sorry, I couldn't respond right now. {exc}\n")


if __name__ == "__main__":
    chat()