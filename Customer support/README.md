# Customer Support Bot with Memory
### Built with Python and Azure AI Foundry

---

## What This Project Does

This is a terminal-based customer support chatbot that demonstrates **four important memory concepts** used in real AI applications. You chat with it in the terminal, and it remembers information about your problem across the conversation — just like a real support agent would.

The bot:
- Remembers what you said earlier in the conversation
- Tracks your support issue, its status, and what has been tried
- Builds a running summary of important facts
- Only sends relevant memory to the AI model (not everything)

---

## Project Structure

```
customer_support_bot/
│
├── .venv/                  ← Virtual environment (created by you)
├── main.py                 ← The main chatbot application
├── .env                    ← Your API key (never share this file)
├── memory.json             ← Where the bot stores its memory
├── requirements.txt        ← Python packages needed
└── README.md               ← This file
```

---

## Setup Instructions (Windows)

### Step 1 – Create the Virtual Environment

Open a terminal (Command Prompt or PowerShell) inside the project folder and run:

```cmd
python -m venv .venv
```

This creates a folder called `.venv` that holds a private Python installation just for this project.

### Step 2 – Activate the Virtual Environment

```cmd
.venv\Scripts\activate
```

You will see `(.venv)` appear at the beginning of your terminal line. This means the virtual environment is active.

> **Important:** Always activate the virtual environment before running the project.

### Step 3 – Install the Required Packages

```cmd
pip install -r requirements.txt
```

This installs the `openai` and `python-dotenv` libraries inside the virtual environment.

### Step 4 – Create the `.env` File

Open the `.env` file in the project folder and replace the placeholder with your real API key:

```
AZURE_API_KEY=paste_your_real_api_key_here
```

> **Never share your `.env` file or commit it to GitHub.** It contains a secret key.

### Step 5 – Run the Application

```cmd
python main.py
```

---

## How to Use the Bot

Once running, you will see a welcome message. Just type your support question and press **Enter**.

**Special commands:**

| Command | What it does |
|---|---|
| `memory` | Shows what the bot currently remembers |
| `exit`, `bye`, `quit` | Clears memory and closes the application |

**Example conversation:**

```
You: My Wi-Fi isn't working.
Bot: Have you tried restarting your router?

You: Yes, I already restarted the router.
Bot: I see. Since restarting didn't help, let's try...

You: It is working now.
Bot: That's great! I'm glad we could resolve your issue.
```

---

## The Four Memory Concepts Explained

### 1. Short-Term Memory

**What it is:**
Short-term memory is the list of messages exchanged in the current conversation. It works exactly like your own short-term memory — you remember what was said a few moments ago.

**How it works in the code:**
Every time you send a message and the bot replies, both messages are saved in a list called `conversation_history`. Before the next call to the AI, the last few messages from this list are included so the AI knows what was recently said.

**Why it matters:**
Without this, the bot would forget everything you said the moment you send your next message. It would be like talking to someone who has amnesia every second.

**In `main.py`:**
```python
memory["conversation_history"].append({"role": "user", "content": user_input})
```

---

### 2. Summary-Based Memory

**What it is:**
Instead of keeping every single message ever said, the bot asks the AI to write a short bullet-point summary of the important facts after each exchange. This is like a nurse writing case notes during a doctor's appointment.

**How it works in the code:**
After each reply, the `update_summary()` function sends the previous summary plus the latest exchange to the AI and asks it to produce an updated 3–5 bullet summary containing only technical facts — no small talk.

**Why it matters:**
Conversations can get very long. Sending the entire history every time would be slow and expensive. A compact summary keeps things efficient while preserving the key facts.

**Example summary:**
```
- Customer reported Wi-Fi is not connecting.
- Router has been restarted — issue persists.
- Next steps: check IP address settings.
```

**In `main.py`:**
```python
def update_summary(client, memory, user_message, assistant_reply):
```

---

### 3. State Tracking

**What it is:**
State tracking means the bot keeps a structured record of the support case — like a ticket in a helpdesk system. It tracks:

- **issue** – what the problem is (e.g., "Wi-Fi not working")
- **status** – `open`, `in-progress`, or `resolved`
- **attempts** – a list of things that have already been tried

**How it works in the code:**
The `update_issue_state()` function reads the user's message and updates these fields automatically. If the user says "it's working now", the status changes to `resolved`. If the user mentions they restarted the router, "Restarted router" is added to the attempts list.

**Why it matters:**
This prevents the bot from suggesting the same step twice. If you already restarted the router, the bot will not tell you to restart it again.

**In `memory.json`:**
```json
{
    "issue": "Wi-Fi not working",
    "status": "in-progress",
    "attempts": ["Restarted router"]
}
```

**In `main.py`:**
```python
def update_issue_state(memory, user_message, assistant_reply):
```

---

### 4. Selective Memory Injection

**What it is:**
This is the most important concept. Instead of dumping all stored memory into every AI request, the bot carefully selects only the most relevant pieces and creates a small, focused context.

**How it works in the code:**
The `create_memory_context()` function builds a short text block like this:

```
[Relevant customer memory]

Issue:
Wi-Fi not working

Status:
in-progress

Previous troubleshooting (DO NOT suggest these again):
- Restarted router

Conversation summary:
- Customer has Wi-Fi issue. Router restart did not help.
```

This block is then prepended to the user's current question and sent to the AI. The AI sees the right context without being overwhelmed by unnecessary information.

**Why it matters:**
Sending everything to the AI every time would be wasteful. Selective injection keeps the prompt focused, faster, and cheaper — and produces better responses.

**In `main.py`:**
```python
def create_memory_context(memory):
```

---

## Code Walkthrough

Here is a simple summary of what each function does:

| Function               | Purpose                                              |
|------------------------|------------------------------------------------------|
| `load_memory()`        | Reads `memory.json` from disk at startup             |
| `save_memory()`        | Writes updated memory to `memory.json` after each turn |
| `update_issue_state()` | Updates issue, status, and attempts from conversation |
| `create_memory_context()` | Builds a focused memory string for the AI prompt  |
| `update_summary()`     | Asks the AI to write a fresh bullet-point summary    |
| `ask_agent()`          | Assembles the full prompt and calls the AI API       |
| `print_banner()`       | Displays the welcome screen                          |
| `display_memory()`     | Prints the current memory when you type `memory`     |
| `main()`               | Runs the main chat loop                              |

---

## Troubleshooting

**"ERROR: Please set your AZURE_API_KEY in the .env file."**
→ Open `.env` and replace `your_api_key_here` with your real API key.

**"ModuleNotFoundError: No module named 'openai'"**
→ Make sure your virtual environment is activated (`.venv\Scripts\activate`) and run `pip install -r requirements.txt`.

**The bot suggests a step I already tried**
→ Type `memory` and check if the attempt was recorded. The bot only avoids steps that appear in the `attempts` list.

**I want to start a fresh conversation**
→ Delete `memory.json` or replace its contents with:
```json
{
    "summary": "",
    "issue": "",
    "status": "open",
    "attempts": [],
    "conversation_history": []
}
```

---

## Technology Used

| Technology      | Purpose                                  |
|-----------------|------------------------------------------|
| Python 3.10+    | Programming language                     |
| openai          | Python SDK for calling the AI model      |
| python-dotenv   | Loads the API key from the `.env` file   |
| Azure AI Foundry | Hosts the AI model (`gpt-5-mini`)       |
| `memory.json`   | Simple file-based memory storage         |
