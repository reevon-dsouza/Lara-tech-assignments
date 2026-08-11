"""Email Validator - Simple checks on generated emails."""

import re


def validate_email(email):
    """Run all checks. Returns list of (check_name, passed, message)."""
    checks = []

    # Has subject?
    has_subject = bool(email.get("subject", "").strip())
    checks.append(("Subject present", has_subject))

    # Has body?
    has_body = bool(email.get("body", "").strip())
    checks.append(("Body present", has_body))

    # No unresolved {placeholders}?
    text = email.get("subject", "") + " " + email.get("body", "")
    placeholders = re.findall(r"\{[a-zA-Z_]+\}", text)
    checks.append(("No unresolved placeholders", len(placeholders) == 0))

    # Formatting ok?
    good_format = len(email.get("subject", "")) <= 200 and len(email.get("body", "")) >= 20
    checks.append(("Formatting valid", good_format))

    return checks


def print_validation(checks):
    """Print validation results."""
    print("\nValidation:")
    for name, passed in checks:
        icon = "✓" if passed else "✗"
        print(f"  {icon} {name}")
