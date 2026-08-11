import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Azure AI Search details
ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

if not API_KEY or not ENDPOINT or not INDEX_NAME:
    raise ValueError("Missing Azure AI Search environment variables in .env file.")

# Create search client
search_client = SearchClient(
    endpoint=ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(API_KEY)
)

# Azure OpenAI details
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

if not OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT or not DEPLOYMENT_NAME:
    raise ValueError("Missing Azure OpenAI environment variables in .env file.")

openai_client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT,
    api_key=OPENAI_API_KEY
)


# System instruction for strict RAG behavior
SYSTEM_INSTRUCTION = """You are a document question-answering assistant.

Answer ONLY using the information provided in the CONTEXT.

Rules:
- Do not use your general knowledge.
- Do not make assumptions.
- Do not invent information.
- Do not hallucinate.
- If the answer is not clearly supported by the CONTEXT, respond exactly:
  'I am not sure about that based on the available documents.'
- If the context contains insufficient information to answer confidently, respond exactly:
  'I am not sure about that based on the available documents.'
- If the documents contain conflicting information, do not choose an answer using general knowledge. Clearly mention that the documents contain conflicting information.
- Keep the answer concise and directly answer the user's question."""


# Search function
def search_documents(query):
    results = search_client.search(
        search_text=query,
        top=5
    )

    documents = []
    for result in results:
        documents.append({
            "content": result.get("content", ""),
            "metadata_storage_name": result.get("metadata_storage_name", "Unknown"),
            "metadata_storage_path": result.get("metadata_storage_path", "")
        })

    return documents


# Generate answer using Azure OpenAI
def generate_answer(question, documents):
    # Build clean context from retrieved documents
    context_parts = []
    sources = []

    for doc in documents:
        source_name = doc["metadata_storage_name"]
        content = doc["content"]

        if content:
            context_parts.append(f"Source: {source_name}\n\n{content}")
            if source_name not in sources:
                sources.append(source_name)

    context = "\n\n---\n\n".join(context_parts)

    # Build the prompt
    user_message = f"""CONTEXT:

{context}

---

QUESTION: {question}"""

    try:
        response = openai_client.responses.create(
            model=DEPLOYMENT_NAME,
            input=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": user_message}
            ]
        )

        answer = response.output_text
        return answer, sources

    except Exception as e:
        print(f"\nBot: Sorry, something went wrong while generating the answer: {e}")
        return None, []


# Main chatbot loop
def main():
    print("=" * 60)
    print("  RAG AI Chatbot (Azure AI Search + Azure OpenAI)")
    print("  Type 'exit' or 'quit' to stop.")
    print("=" * 60)
    print()

    while True:
        question = input("Enter your question: ").strip()

        # Exit condition
        if question.lower() in ("exit", "quit"):
            print("\nGoodbye!")
            break

        # Skip empty input
        if not question:
            continue

        # Step 1: Search documents using existing Azure AI Search
        documents = search_documents(question)

        # Step 2: If no results, respond without calling the LLM
        if not documents:
            print("\nBot: I am not sure about that based on the available documents.\n")
            continue

        # Step 3: Generate answer using Azure OpenAI
        answer, sources = generate_answer(question, documents)

        if answer:
            print(f"\nBot: {answer}")

            # Print sources
            if sources:
                print("\nSources:")
                for source in sources:
                    print(f"- {source}")

            print()


if __name__ == "__main__":
    main()
