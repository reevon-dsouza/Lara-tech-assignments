"""Email Generator - Sends prompts to Azure OpenAI and parses the response."""

import os
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Load environment variables from .env file
load_dotenv()

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://agentic-training2026.services.ai.azure.com/openai/v1")
MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-5-mini")


def get_client():
    """
    Create and configure the Azure OpenAI client.
    
    Checks if an API key is available in the environment (.env).
    If a valid API key is present, it initializes the client using the key.
    Otherwise, it falls back to Entra ID (DefaultAzureCredential) token authentication.
    
    Returns:
        OpenAI: An configured instance of the OpenAI client.
    """
    api_key = os.getenv("AZURE_OPENAI_API_KEY")

    if api_key and api_key != "your_azure_openai_api_key_here":
        return OpenAI(base_url=ENDPOINT, api_key=api_key)

    # Fallback to Azure Credential Token Provider
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )
    return OpenAI(base_url=ENDPOINT, api_key=token_provider)


def generate_email(prompt, client=None):
    """
    Sends the compiled prompt to the Azure OpenAI LLM to generate the email text.
    
    Args:
        prompt (str): The formatted prompt containing instructions and user details.
        client (OpenAI, optional): An existing OpenAI client instance. If None, one is created.
        
    Returns:
        str: The raw generated output text from the language model response.
    """
    if client is None:
        client = get_client()
    response = client.responses.create(model=MODEL, input=prompt)
    return response.output_text


def parse_email(raw_text):
    """
    Parses the raw text response from the model into subject and body components.
    
    Expects the response to follow a format with 'Subject:' and 'Body:' headers.
    It reads line-by-line, extracting the subject text, and accumulates all
    subsequent lines following the 'Body:' header into the body content.
    
    Args:
        raw_text (str): The raw string output returned by the LLM.
        
    Returns:
        dict: A dictionary containing:
            - 'subject' (str): The extracted subject line (default is empty string).
            - 'body' (str): The extracted body content (default is empty string).
    """
    subject, body, in_body = "", "", False
    for line in raw_text.strip().split("\n"):
        if line.lower().startswith("subject:") and not in_body:
            subject = line.split(":", 1)[1].strip()
        elif line.lower().startswith("body:"):
            in_body = True
        elif in_body:
            body += line + "\n"
    return {"subject": subject, "body": body.strip()}
