"""Tests for the Email Automation System."""

import pytest
from unittest.mock import MagicMock
from prompt_library import get_template, list_templates
from email_generator import parse_email, generate_email
from email_validator import validate_email


# --- Template Tests ---

def test_get_valid_template():
    assert get_template("welcome") is not None
    assert get_template("Welcome")["name"] == "Welcome Email"
    assert get_template("WELCOME")["name"] == "Welcome Email"


def test_invalid_template():
    assert get_template("fake") is None


def test_list_templates():
    names = list_templates()
    assert len(names) == 8


def test_new_templates_exist():
    assert get_template("feedback") is not None
    assert get_template("outreach") is not None
    assert get_template("thank_you") is not None
    assert get_template("announcement") is not None


# --- Email Generation (Mocked & Custom Prompts) ---

def test_generate_email():
    mock_client = MagicMock()
    mock_client.responses.create.return_value = MagicMock(
        output_text="Subject: Hi\nBody:\nHello, this is a test email body text."
    )
    result = generate_email("test prompt", client=mock_client)
    assert "Subject: Hi" in result


def test_custom_prompt_generation():
    custom_prompt = "Write an apology email to John for the delay"
    formatted_prompt = f"{custom_prompt}\n\nFormat as:\nSubject: <subject>\nBody:\n<body>"
    assert "John" in formatted_prompt
    assert "Format as:" in formatted_prompt


# --- Parsing Tests ---

def test_parse_email():
    raw = "Subject: Hello\nBody:\nThis is the email body content here."
    email = parse_email(raw)
    assert email["subject"] == "Hello"
    assert "email body" in email["body"]


def test_parse_empty():
    email = parse_email("just plain text")
    assert email["subject"] == ""
    assert email["body"] == ""


# --- Validation Tests ---

def test_valid_email_passes():
    email = {"subject": "Welcome", "body": "Hello! Welcome to our platform. We are glad to have you."}
    checks = validate_email(email)
    assert all(passed for _, passed in checks)


def test_empty_subject_fails():
    email = {"subject": "", "body": "This is a valid body with enough words."}
    checks = validate_email(email)
    assert not dict(checks)["Subject present"]


def test_empty_body_fails():
    email = {"subject": "Hi", "body": ""}
    checks = validate_email(email)
    assert not dict(checks)["Body present"]


def test_unresolved_placeholders():
    email = {"subject": "Hello {name}", "body": "Welcome to {company}! Enjoy your stay with us."}
    checks = validate_email(email)
    assert not dict(checks)["No unresolved placeholders"]


# --- Edge Cases ---

def test_special_characters():
    template = get_template("welcome")
    filled = template["prompt"].format(recipient_name="José 😊", company_name="Café ☕")
    assert "José 😊" in filled


def test_long_input():
    template = get_template("welcome")
    filled = template["prompt"].format(recipient_name="A" * 500, company_name="TestCo")
    assert "A" * 500 in filled


def test_missing_fields():
    template = get_template("welcome")
    with pytest.raises(KeyError):
        template["prompt"].format(recipient_name="Alice")
