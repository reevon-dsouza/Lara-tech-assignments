import sys
import os
from dotenv import load_dotenv

# Ensure UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Import the three specialized agent modules
from research_agent import research_agent
from summarizer import summarize
from reporter import generate_report

# Load environment variables
load_dotenv()


def check_environment():
    """
    Validate presence of required environment variables before running pipeline.
    Prints informative warning if any variables are missing.
    """
    required_vars = ["PROJECT_ENDPOINT", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var) or os.getenv(var) in ["your_api_key_here", "<your-api-key>"]]

    if missing:
        print("\n[WARNING] Configuration Check:")
        print(f" - Missing or unconfigured environment variables: {', '.join(missing)}")
        print(" Please update your .env file with your Azure credentials before proceeding.\n")


def run_pipeline(topic: str):
    """
    Executes the 3-agent sequential workflow:
    Topic -> Research Agent (Foundry API) -> Summarizer Agent (Azure OpenAI) -> Reporter Agent (Azure OpenAI) -> Final Output
    """
    print("\n" + "=" * 40)
    print("       MULTI-AGENT NEWS PIPELINE")
    print("=" * 40)
    print(f"\nTarget Topic: {topic}\n")

    # ----------------------------------------------------
    # Stage 1: Research Agent (Azure AI Foundry Agent API)
    # ----------------------------------------------------
    print("[1/3] Research Agent")
    print("Using Azure AI Foundry Agent API...")
    print("Researching topic...")
    try:
        research_result = research_agent(topic)
        print("Research completed.")
    except Exception as e:
        print(f"\n[ERROR] Research Agent failed: {e}")
        return

    # ----------------------------------------------------
    # Stage 2: Summarizer Agent (Normal Azure OpenAI API)
    # ----------------------------------------------------
    print("\n[2/3] Summarizer Agent")
    print("Using normal Azure OpenAI API...")
    print("Summarizing research...")
    try:
        summary_result = summarize(research_result)
        print("Summary completed.")
    except Exception as e:
        print(f"\n[ERROR] Summarizer Agent failed: {e}")
        return

    # ----------------------------------------------------
    # Stage 3: Reporter Agent (Normal Azure OpenAI API)
    # ----------------------------------------------------
    print("\n[3/3] Reporter Agent")
    print("Using normal Azure OpenAI API...")
    print("Generating final report...")
    try:
        final_report = generate_report(summary_result)
        print("Report completed.")
    except Exception as e:
        print(f"\n[ERROR] Reporter Agent failed: {e}")
        return

    # ----------------------------------------------------
    # Display Final Report
    # ----------------------------------------------------
    print("\n" + "=" * 40)
    print("              FINAL REPORT")
    print("=" * 40 + "\n")
    
    # Safely print report with utf-8 fallback handling
    try:
        print(final_report)
    except UnicodeEncodeError:
        print(final_report.encode('ascii', errors='replace').decode('ascii'))
        
    print("\n" + "=" * 40 + "\n")


def main():
    """
    Main application loop. Prompts user for topic input until exit or quit.
    """
    print("========================================")
    print("  WELCOME TO MULTI-AGENT NEWS PIPELINE")
    print("========================================")
    
    check_environment()

    while True:
        try:
            topic = input("Enter a news topic (or type 'exit' to quit): ").strip()
            
            if not topic:
                print("Topic cannot be empty. Please enter a valid news topic.")
                continue

            if topic.lower() in ["exit", "quit"]:
                print("\nExiting Multi-Agent News Pipeline. Goodbye!")
                break

            run_pipeline(topic)

        except (KeyboardInterrupt, EOFError):
            print("\nProgram interrupted. Exiting.")
            sys.exit(0)


if __name__ == "__main__":
    main()
