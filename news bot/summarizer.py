import os
from dotenv import load_dotenv
from openai import OpenAI, AzureOpenAI

# Load environment variables
load_dotenv()

# Global cached client to reuse TCP/SSL connections
_cached_client = None


def _get_client():
    global _cached_client
    if _cached_client is None:
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv(
            "AZURE_OPENAI_ENDPOINT",
            "https://agentic-training2026.services.ai.azure.com/openai/v1"
        )
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

        if not api_key or api_key in ["your_api_key_here", "<your-api-key>"]:
            raise ValueError("AZURE_OPENAI_API_KEY is missing or invalid in .env file.")

        if "/openai/v1" in endpoint or "services.ai.azure.com" in endpoint:
            _cached_client = OpenAI(base_url=endpoint, api_key=api_key)
        else:
            _cached_client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version=api_version)

    return _cached_client


def summarize(research_output: dict) -> str:
    """
    Summarizer Agent: High-speed summarization using cached OpenAI client.
    """
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-mini")
    client = _get_client()

    system_prompt = (
        "You are the Summarizer Agent. Analyze the provided research.\n"
        "Filter out noise and duplicates. Extract the key facts and preserve all original sources.\n"
        "Be concise and fast. Output strictly in format:\n"
        "SUMMARY:\n<summary text>\n\n"
        "KEY FACTS:\n1. ...\n2. ...\n\n"
        "SOURCES:\n1. <source name> - <article title> - <URL>"
    )

    topic = research_output.get("topic", "")
    raw_research = research_output.get("raw_research", "")

    user_content = f"TOPIC: {topic}\n\nRESEARCH DATA:\n{raw_research}"

    output_text = None
    try:
        if hasattr(client, "responses"):
            response = client.responses.create(
                model=deployment,
                input=f"{system_prompt}\n\n{user_content}"
            )
            output_text = getattr(response, "output_text", None)
            if not output_text and hasattr(response, "output") and response.output:
                output_text = response.output[0] if isinstance(response.output, list) else str(response.output)

        if not output_text:
            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ]
            )
            output_text = response.choices[0].message.content
    except Exception:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        )
        output_text = response.choices[0].message.content

    if not output_text or not str(output_text).strip():
        raise ValueError("Summarizer Agent received an empty output.")

    return str(output_text).strip()
