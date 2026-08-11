import os

from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

# Azure AI configuration
endpoint = "https://Agentic-training2026.services.ai.azure.com/openai/v1"
deployment_name = "gpt-5-mini"

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url=endpoint,
    api_key=os.environ["AZURE_OPENAI_API_KEY"]
)


# Misleading words / phrases
blocked_words = [
    "guaranteed",
    "100% guaranteed",
    "guarantee",
    "no risk",
    "risk free",
    "zero risk",

    "best in the world",
    "world's best",
    "number one",
    "#1",
    "the best",
    "unbeatable",
    "never fails",
    "always works",

    "get rich quick",
    "instant wealth",
    "easy money",
    "double your money",
    "guaranteed profit",
    "guaranteed returns",
    "risk-free investment",

    "instant results",
    "instant success",
    "instant transformation",
    "works instantly",
    "results guaranteed",
    "100% effective",
    "works every time",

    "miracle cure",
    "cures",
    "cure",
    "heals instantly",
    "guaranteed weight loss",
    "lose weight instantly",

    "scientifically proven",
    "clinically proven",
    "doctor approved",
    "expert approved",
    "proven to work",
    "proven results",

    "better than everyone",
    "better than all",
    "no competitor",
    "unmatched",
    "number one product"
]


def contains_blocked_word(text):
    text = text.lower()

    for word in blocked_words:
        if word in text:
            return True, word

    return False, None


def generate_slogan(product, audience, campaign_goal):

    # Check user input
    user_input = f"{product} {audience} {campaign_goal}"

    blocked, word = contains_blocked_word(user_input)

    if blocked:
        return f"Request blocked because it contains a potentially misleading claim: '{word}'"

    # Generate slogans
    prompt = f"""
Generate 5 marketing slogans.

Product: {product}
Target audience: {audience}
Campaign goal: {campaign_goal}

Rules:
- Keep slogans short and memorable.
- Do not make misleading claims.
- Do not invent statistics.
- Do not make unsupported guarantees.
- Do not claim to be the world's best or number one.
- Do not make medical claims.
- Do not promise unrealistic results.

Number the slogans from 1 to 5.
"""

    response = client.responses.create(
        model=deployment_name,
        input=prompt
    )

    slogans = response.output_text

    # Check generated slogans
    blocked, word = contains_blocked_word(slogans)

    if blocked:
        return "Generated content blocked because it contains a potentially misleading claim."

    return slogans


def main():
    print("=== Marketing Slogan Generator ===")
    print("Type 'quit' or 'exit' to quit at any time.\n")

    while True:
        try:
            product = input("Product: ").strip()
            if product.lower() in ("quit", "exit"):
                print("\nGoodbye!")
                break
            if not product:
                continue

            audience = input("Target audience: ").strip()
            if audience.lower() in ("quit", "exit"):
                print("\nGoodbye!")
                break

            campaign_goal = input("Campaign goal: ").strip()
            if campaign_goal.lower() in ("quit", "exit"):
                print("\nGoodbye!")
                break

            print("\nGenerating slogan...")
            result = generate_slogan(product, audience, campaign_goal)

            print("\nResult:")
            print(result)
            print("\n" + "-" * 40 + "\n")

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
