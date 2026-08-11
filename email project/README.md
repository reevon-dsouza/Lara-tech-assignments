# Email Automation Testing System

Simple Python project using Azure OpenAI (`gpt-5-mini`) to generate and validate emails.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Test

```bash
pytest -v
```

## Project Structure

```
email_automation/
├── .venv/
├── main.py              # Terminal interface
├── prompt_library.py    # Email templates
├── email_generator.py   # Azure OpenAI calls
├── email_validator.py   # Email validation
├── tests/
│   └── test_email.py    # Tests
├── requirements.txt
└── README.md
```
