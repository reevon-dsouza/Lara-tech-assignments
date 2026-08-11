# Multi-Agent News Pipeline

A complete, beginner-friendly Python application demonstrating a 3-agent sequential workflow built with **Azure AI Foundry Agent API** and **Normal Azure OpenAI API**.

---

## 1. Project Overview

The **Multi-Agent News Pipeline** automates news gathering, summarization, and reporting by decomposing complex news production into three specialized autonomous agents:

1. **Research Agent** (Azure AI Foundry Agent API): Conducts web research, collects facts, and retrieves verified sources.
2. **Summarizer Agent** (Normal Azure OpenAI API): Filters out noise, removes duplicates, and organizes key facts with their original sources.
3. **Reporter Agent** (Normal Azure OpenAI API): Formulates a compelling headline and writes a professional, neutral news report with full source citations.

---

## 2. Objective

The primary objective of this project is to demonstrate key multi-agent design principles:
- **Task Decomposition**: Dividing complex workflows into manageable steps.
- **Specialized Skills**: Assigning optimal tools and prompts to distinct agents.
- **Coordinated Output**: Passing structured data seamlessly from stage to stage.
- **Source Traceability & Provenance**: Ensuring factual citations and URLs are preserved from web research through to the final article without fabrication.

---

## 3. Multi-Agent Architecture & API Distinction

| Agent | API Approach | Python Module | Key Responsibilities |
| :--- | :--- | :--- | :--- |
| **Research Agent** | **Azure AI Foundry Agent API** (`azure-ai-projects` SDK) | [`research_agent.py`](file:///d:/lara%20tech/news%20bot/research_agent.py) | Web research, fact gathering, source & citation extraction. |
| **Summarizer Agent** | **Normal Azure OpenAI API** (`openai.AzureOpenAI` SDK) | [`summarizer.py`](file:///d:/lara%20tech/news%20bot/summarizer.py) | Content filtering, deduplication, key fact extraction, source preservation. |
| **Reporter Agent** | **Normal Azure OpenAI API** (`openai.AzureOpenAI` SDK) | [`reporter.py`](file:///d:/lara%20tech/news%20bot/reporter.py) | News article drafting, headline creation, source section formatting. |

> [!NOTE]
> The Research Agent uses the specialized **Azure AI Foundry Agent API** with integrated web/news search capabilities, while the Summarizer and Reporter Agents use standard **Azure OpenAI API completions** without web access.

---

## 4. Sequential Data Flow

```
                  USER TOPIC
                      │
                      ▼
            ┌───────────────────┐
            │  RESEARCH AGENT   │  <-- Azure AI Foundry Agent API
            └─────────┬─────────┘
                      │  (Research Text + Citations/Sources)
                      ▼
            ┌───────────────────┐
            │ SUMMARIZER AGENT  │  <-- Normal Azure OpenAI API
            └─────────┬─────────┘
                      │  (Summary + Key Facts + Sources)
                      ▼
            ┌───────────────────┐
            │  REPORTER AGENT   │  <-- Normal Azure OpenAI API
            └─────────┬─────────┘
                      │  (Headline + Article + Preserved Sources)
                      ▼
          FINAL NEWS REPORT + SOURCES
```

---

## 5. Project Structure

```
multi_agent_news_pipeline/
│
├── main.py              # CLI entry point orchestrating agent execution flow
├── research_agent.py    # Research Agent (Azure AI Foundry Agent API)
├── summarizer.py        # Summarizer Agent (Normal Azure OpenAI API)
├── reporter.py          # Reporter Agent (Normal Azure OpenAI API)
├── .env                 # Local environment credentials (git-ignored)
├── .env.example         # Example environment template
├── requirements.txt     # Python project dependencies
└── README.md            # Complete project documentation
```

---

## 6. Environment Variables Setup

Create a `.env` file in the root directory (or copy from `.env.example`):

```env
# ==================================================
# Azure AI Foundry Agent Configuration (Research Agent)
# ==================================================
PROJECT_ENDPOINT=https://your-project-name.region.inference.ai.azure.com
# Alternatively: PROJECT_CONNECTION_STRING=...
FOUNDRY_AGENT_ID=asst_your_agent_id_here

# ==================================================
# Normal Azure OpenAI Configuration (Summarizer & Reporter)
# ==================================================
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-08-01-preview
```

### Credential Explanation:
- `PROJECT_ENDPOINT`: Azure AI Foundry project endpoint URL.
- `FOUNDRY_AGENT_ID`: ID of an existing Agent configured in Azure AI Foundry with search capabilities (e.g. Bing Search tool).
- `AZURE_OPENAI_ENDPOINT`: Endpoint URL for your Azure OpenAI Service resource.
- `AZURE_OPENAI_API_KEY`: API key for your Azure OpenAI Service resource.
- `AZURE_OPENAI_DEPLOYMENT`: Deployment name of your chat model (e.g. `gpt-4o`).

---

## 7. Azure Setup Guide

1. **Azure AI Foundry Agent**:
   - Navigate to [Azure AI Foundry Portal](https://ai.azure.com/).
   - Open your project and go to **Agents**.
   - Create or select an existing agent with **Bing Search** or **Web Search** tools enabled.
   - Copy the `Agent ID` (format: `asst_...`) and place it in `FOUNDRY_AGENT_ID`.

2. **Azure OpenAI Deployment**:
   - Deploy a chat model (e.g., `gpt-4o` or `gpt-4`) in your Azure OpenAI resource.
   - Copy the deployment name, endpoint URL, and API key into `.env`.

---

## 8. Virtual Environment & Installation (Windows)

All dependencies **must** be installed inside a Python virtual environment to avoid installing packages globally.

### Step 1: Open Terminal in Project Folder

Navigate to the project root directory.

### Step 2: Create Virtual Environment

```cmd
python -m venv .venv
```

### Step 3: Activate Virtual Environment

```cmd
.venv\Scripts\activate
```

*(You should see `(.venv)` displayed at the beginning of your terminal prompt).*

### Step 4: Install Dependencies

```cmd
pip install -r requirements.txt
```

---

## 9. Running the Application

Make sure `.venv` is activated and `.env` is configured.

```cmd
python main.py
```

### Deactivating the Environment

When finished working, deactivate the virtual environment:

```cmd
deactivate
```

---

## 10. Example Input & Output

### Terminal Progress Execution

```text
========================================
  WELCOME TO MULTI-AGENT NEWS PIPELINE
========================================

Enter a news topic (or type 'exit' to quit): Quantum Computing Breakthroughs

========================================
       MULTI-AGENT NEWS PIPELINE
========================================

Target Topic: Quantum Computing Breakthroughs

[1/3] Research Agent
Using Azure AI Foundry Agent API...
Researching topic...
Research completed.

[2/3] Summarizer Agent
Using normal Azure OpenAI API...
Summarizing research...
Summary completed.

[3/3] Reporter Agent
Using normal Azure OpenAI API...
Generating final report...
Report completed.

========================================
              FINAL REPORT
========================================

========================================
FINAL NEWS REPORT
========================================

HEADLINE:
Next-Gen Quantum Processors Reach 1,000-Qubit Milestone in Error Correction

REPORT:

Recent breakthroughs in quantum computing have accelerated the transition from theoretical research to practical application. Leading laboratories have demonstrated fault-tolerant logical qubits operating with significantly lower error rates...

SOURCES:

1. Nature Quantum Information
   Fault-Tolerant Quantum Operations Achieved
   https://www.nature.com/articles/example-quantum-1

2. MIT Technology Review
   1000-Qubit Milestone Reached
   https://www.technologyreview.com/example-quantum-2

========================================
```

---

## 11. Source & Citation Provenance

Sources are preserved end-to-end throughout the multi-agent pipeline:
- **Research Agent**: Captures raw facts, article titles, source publishers, URLs, and Bing citation annotations.
- **Summarizer Agent**: Maintains verified source tags alongside key facts while removing duplicate claims.
- **Reporter Agent**: Embeds the exact, un-modified source titles and URLs in the final report section.

> [!WARNING]
> None of the agents are permitted to fabricate sources, URLs, or factual assertions. Every source in the final output originates directly from actual research results.

---

## 12. Error Handling

The application includes robust error checks for:
- Missing or placeholder `.env` configuration keys.
- Azure AI Foundry client authentication and thread errors.
- Empty agent or model response payloads.
- Network connection failures and API timeouts.
