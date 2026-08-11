import os
import time
from dotenv import load_dotenv
from azure.core.credentials import TokenCredential, AccessToken
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient  # type: ignore

# Load environment variables from .env file
load_dotenv()


class KeyTokenCredential(TokenCredential):
    """Custom TokenCredential wrapper for API Key authentication."""
    def __init__(self, key: str):
        self.key = key

    def get_token(self, *scopes, **kwargs) -> AccessToken:
        return AccessToken(self.key, int(time.time()) + 3600)


# Global cached clients to avoid SSL handshake overhead on repeated calls
_cached_project_client = None
_cached_openai_client = None


def _get_openai_client():
    global _cached_project_client, _cached_openai_client
    if _cached_openai_client is None:
        project_endpoint = os.getenv(
            "PROJECT_ENDPOINT",
            "https://agentic-training2026.services.ai.azure.com/api/projects/Batch2026"
        )
        api_key = os.getenv("AZURE_OPENAI_API_KEY")

        if api_key and api_key not in ["your_api_key_here", "<your-api-key>"]:
            credential = KeyTokenCredential(api_key)
        else:
            credential = DefaultAzureCredential()

        _cached_project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=credential,
        )
        _cached_openai_client = _cached_project_client.get_openai_client()

    return _cached_openai_client


def research_agent(topic: str) -> dict:
    """
    Research Agent: Optimized for high-speed execution using Azure AI Foundry Agent API.
    """
    agent_name = os.getenv("FOUNDRY_AGENT_NAME", os.getenv("FOUNDRY_AGENT_ID", "ReevonAgent"))
    agent_version = os.getenv("FOUNDRY_AGENT_VERSION", "5")

    # Get cached client
    openai_client = _get_openai_client()

    # Concise research prompt for fast, focused generation
    research_prompt = (
        "You are the Research Agent. Research the requested topic using web/search tools.\n"
        "Provide recent key facts, source names, article titles, and URLs.\n"
        "Be factual and concise. Do not write a full news article.\n\n"
        f"Topic: {topic}"
    )

    try:
        response = openai_client.responses.create(
            input=[{"role": "user", "content": research_prompt}],
            extra_body={
                "agent_reference": {
                    "name": agent_name,
                    "version": str(agent_version),
                    "type": "agent_reference"
                }
            },
        )
    except Exception as primary_error:
        # Fallback to direct thread/run execution if needed
        try:
            agent = _cached_project_client.agents.get_agent(agent_id=agent_name)
            thread = _cached_project_client.agents.create_thread()
            _cached_project_client.agents.create_message(thread_id=thread.id, role="user", content=research_prompt)
            run = _cached_project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
            messages = _cached_project_client.agents.list_messages(thread_id=thread.id)
            output_text = ""
            for msg in messages.data:
                if msg.role == "assistant":
                    for block in msg.content:
                        if hasattr(block, "text"):
                            output_text += block.text.value + "\n"
                    break
            class FallbackResponse:
                pass
            response = FallbackResponse()
            response.output_text = output_text
        except Exception as fallback_error:
            raise RuntimeError(f"Azure AI Foundry Agent failed: {primary_error} ({fallback_error})")

    # Extract output text
    output_text = getattr(response, "output_text", None)
    if not output_text and hasattr(response, "output") and response.output:
        output_text = response.output[0] if isinstance(response.output, list) else str(response.output)
    if not output_text and hasattr(response, "choices") and response.choices:
        output_text = response.choices[0].message.content

    if not output_text or not str(output_text).strip():
        raise ValueError("Research Agent returned an empty response.")

    return {
        "topic": topic,
        "raw_research": str(output_text).strip(),
        "citations": []
    }
