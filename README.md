# Lara Tech Assignments

Welcome to the **Lara Tech Assignments** repository. This repository contains a collection of AI-driven projects, autonomous agents, web automation tools, and API test suites built using Python, Google Gemini, OpenAI, FastAPI, and Agno (Phidata).

---

## 📂 Project Overview

| Project Directory | Description | Key Tech / Frameworks |
| :--- | :--- | :--- |
| 🔍 [Ai search](./Ai%20search/) | AI-powered Web Search Agent that queries real-time information and generates synthesis reports. | Google Gemini, DuckDuckGo / Tavily |
| 🎧 [Customer support](./Customer%20support/) | Automated Customer Support Bot handling inquiries and support workflows. | Python, FastAPI / Agno, OpenAI / Gemini |
| ✉️ [email project](./email%20project/) | Dynamic Email Generator & Validator with built-in prompt library and test suite. | Python, Pytest, Gemini API |
| 🏷️ [marketing_slogan_generator](./marketing_slogan_generator/) | Marketing Slogan Generator tool (Streamlit / Web UI app). | Python, Streamlit, Gemini / OpenAI API |
| 📰 [news bot](./news%20bot/) | Autonomous News Research & Reporter Agent that fetches, summarizes, and reports current events. | Python, Multi-agent flow, Tavily / DuckDuckGo Search |
| 🧪 [Test apis](./Test%20apis/) | Sandbox environment for testing LLM APIs, embeddings, and endpoint integrations. | Python, FastAPI / HTTPX |
| 🌤️ [Weather project](./Weather%20project/) | Agentic AI Weather Application providing live weather forecasts and intelligent summaries. | Python, Agno (Phidata), OpenWeatherMap API |

---

## 🛠️ Prerequisites & Setup

### 1. General Prerequisites
- **Python**: Version 3.10+ recommended
- **Package Manager**: `pip` or [`uv`](https://github.com/astral-sh/uv)

### 2. Environment Configuration
Most projects require API keys (e.g., Google Gemini, OpenAI, Tavily, OpenWeatherMap). 
Copy `.env.example` to `.env` inside the respective project folder before running:

```bash
cp .env.example .env  # or rename manually on Windows
```

---

## 🚀 Getting Started

To run any individual project:

```bash
# 1. Navigate to the desired project directory
cd "Ai search" # or "news bot", "email project", etc.

# 2. Set up virtual environment (if needed)
python -m venv .venv
# Activate on Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Activate on Linux/macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the project entry point
python main.py
```

---

## 📑 Detailed Project Documentation

For specific setup, features, and usage details, refer to the individual `README.md` files located in each project folder:
- [Ai search README](./Ai%20search/README.md)
- [Customer support README](./Customer%20support/README.md)
- [email project README](./email%20project/README.md)
- [news bot README](./news%20bot/README.md)
- [Weather project README](./Weather%20project/agentic-ai-weather/README.md)