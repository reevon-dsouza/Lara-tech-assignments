import os
from openai import OpenAI
from dotenv import load_dotenv

# ── 1. Configuration & Settings ────────────────────────────────────────────────
# API endpoint for Azure AI Foundry / Azure OpenAI service
ENDPOINT = "https://agentic-training2026.services.ai.azure.com/openai/v1"
# Target model deployment name
DEPLOYMENT_NAME = "gpt-5-mini"

# Keywords mapped to standardized troubleshooting steps to avoid suggesting duplicate steps
STEPS = [
    ("restart", "Restarted router"), ("reboot", "Rebooted device"),
    ("reset", "Reset settings"),     ("unplug", "Unplugged device"),
    ("reinstall", "Reinstalled app"), ("update", "Updated firmware"),
    ("clear cache", "Cleared cache")
]

# ── 2. Rule-Based State Tracking ───────────────────────────────────────────────
def update_state(mem, msg):
    """
    Scans user messages to update case details:
    - Sets status to 'resolved' when user confirms issue is fixed.
    - Captures the initial problem description if not set yet.
    - Updates case status from 'open' to 'in-progress'.
    - Logs any troubleshooting steps the user mentions trying.
    """
    low = msg.lower()
    
    # 1. Detect resolution keywords
    if any(p in low for p in ["it's working", "it is working", "fixed", "resolved", "working now", "all good"]):
        mem["status"] = "resolved"
        return
        
    # 2. Extract issue description if empty
    if not mem["issue"] and any(k in low for k in ["not working", "issue", "problem", "broken", "error", "can't", "won't", "slow", "offline"]):
        mem["issue"] = msg.strip()[:100]
        
    # 3. Transition status to in-progress
    if mem["issue"] and mem["status"] == "open":
        mem["status"] = "in-progress"
        
    # 4. Log newly attempted troubleshooting steps
    for kw, label in STEPS:
        if kw in low and label not in mem["attempts"]:
            mem["attempts"].append(label)

# ── 3. Selective Memory Context Builder ────────────────────────────────────────
def memory_context(mem):
    """
    Formats active in-memory state (issue, status, attempted troubleshooting steps)
    into a context block dynamically injected into the LLM system prompt.
    """
    ctx = []
    if mem["issue"]: ctx.append(f"Issue:\n{mem['issue']}")
    if mem["status"]: ctx.append(f"Status:\n{mem['status']}")
    if mem["attempts"]: ctx.append("Previous troubleshooting (DO NOT suggest these again):\n" + "\n".join(f"- {a}" for a in mem["attempts"]))
    return ("[Relevant customer memory]\n" + "\n\n".join(ctx) + "\n\n") if ctx else ""

# ── 4. Agent Call & Streaming Prompt Assembly ──────────────────────────────────
def ask_agent(client, mem, user_msg):
    """
    Combines system persona, memory context, and recent history (last 6 turns)
    to stream responses token-by-token from the Azure OpenAI model.
    """
    history = "".join(f"{'Customer' if t['role']=='user' else 'Agent'}: {t['content']}\n" for t in mem["conversation_history"][-6:])
    prompt = (
        "You are a friendly customer support agent. Help solve technical problems step by step. "
        "Never suggest a troubleshooting step already attempted. Congratulate the customer warmly if their issue is resolved.\n\n"
        f"{memory_context(mem)}"
        f"{'[Recent conversation]\n' + history if history else ''}"
        f"Customer: {user_msg}\nAgent:"
    )
    
    stream = client.responses.create(model=DEPLOYMENT_NAME, input=prompt, stream=True)
    full_text = []
    print("\nBot: ", end="", flush=True)
    for event in stream:
        if type(event).__name__ == "ResponseTextDeltaEvent":
            print(event.delta, end="", flush=True)
            full_text.append(event.delta)
    print("\n")
    return "".join(full_text).strip()

# ── 5. Main CLI Loop & In-Memory State Execution ───────────────────────────────
def main():
    # Load environment variables (API Key) from .env
    load_dotenv()
    api_key = os.getenv("AZURE_API_KEY")
    if not api_key:
        print("ERROR: Set AZURE_API_KEY in .env"); return

    # Initialize OpenAI client with Azure AI Foundry endpoint
    client = OpenAI(base_url=ENDPOINT, api_key=api_key)

    # In-memory dictionary maintaining conversation state during runtime execution
    mem = {"issue": "", "status": "open", "attempts": [], "conversation_history": []}

    print("Customer Support Bot\nCommands: 'memory' | 'exit'\nBot: Hello! How can I help you today?\n")
    
    # Interactive CLI loop
    while True:
        try:
            inp = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!"); break
        if not inp: continue
        
        # Exit commands
        if inp.lower() in ["exit", "bye", "quit"]:
            print("Bot: Goodbye!"); break
            
        # Inspect in-memory state
        if inp.lower() == "memory":
            print(f"\nIssue: {mem['issue'] or '(none)'}\nStatus: {mem['status']}\nAttempts: {mem['attempts'] or '(none)'}\nTurns: {len(mem['conversation_history'])}\n")
            continue

        # Step A: Append user message to short-term conversation history
        mem["conversation_history"].append({"role": "user", "content": inp})
        
        # Step B: Stream response from support agent LLM
        try:
            reply = ask_agent(client, mem, inp)
        except Exception as e:
            print(f"\nBot: [API error: {e}]\n")
            mem["conversation_history"].pop()
            continue

        # Step C: Record assistant reply in short-term conversation history
        mem["conversation_history"].append({"role": "assistant", "content": reply})
        
        # Step D: Update memory state tracking (status, issue, attempted steps)
        update_state(mem, inp)

if __name__ == "__main__":
    main()





