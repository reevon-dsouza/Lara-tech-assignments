"""Email Automation Testing System - Terminal Interface."""

import re
from prompt_library import get_template, list_templates
from email_generator import generate_email, parse_email
from email_validator import validate_email, print_validation


def main():
    print("\n=== Email Automation System ===\n")

    # Show templates
    print("Available Templates:")
    templates = list_templates()
    for i, (tid, name) in enumerate(templates, 1):
        print(f"  {i}. {name}")
    print("  0. Custom Prompt (Write your own email prompt)")

    # Pick template or custom prompt
    template = None
    custom_prompt = None

    while not template and not custom_prompt:
        user_input = input("\nSelect option (number, ID, or name, or 0 for custom): ").strip()
        
        # Check if user selected 0 (Custom Prompt)
        if user_input == "0" or user_input.lower() == "custom":
            print("\n→ Custom Email Prompt")
            custom_prompt = input("\nEnter your custom prompt for the email: ").strip()
            if not custom_prompt:
                print("Prompt cannot be empty!")
                custom_prompt = None
                continue
            filled_prompt = f"{custom_prompt}\n\nFormat as:\nSubject: <subject>\nBody:\n<body>"
            break

        # Check if user entered a number (e.g., 1, 2, 3...)
        if user_input.isdigit():
            idx = int(user_input) - 1
            if 0 <= idx < len(templates):
                template_id = templates[idx][0]
                template = get_template(template_id)
        else:
            # Check by ID directly (e.g. 'welcome', 'support')
            template = get_template(user_input)
            
            # Check by Name matching (e.g. 'customer support', 'Welcome Email')
            if not template:
                for tid, name in templates:
                    if user_input.lower() in (tid.lower(), name.lower()):
                        template = get_template(tid)
                        break

        if not template and not custom_prompt:
            print("Invalid selection! Please enter a valid option number, ID, or name.")

    # Fill template prompt if template was selected
    if template:
        print(f"\n→ {template['name']}\n")
        print("Enter your content:")
        content = {}
        fields = re.findall(r"\{(\w+)\}", template["prompt"])
        for field in fields:
            label = field.replace("_", " ").title()
            content[field] = input(f"  {label}: ")

        filled_prompt = template["prompt"].format(**content)

    print("\nGenerating email...")
    raw = generate_email(filled_prompt)

    # Parse and display
    email = parse_email(raw)
    print(f"\nSubject: {email['subject']}")
    print(f"\nBody:\n{email['body']}")

    # Validate
    checks = validate_email(email)
    print_validation(checks)


if __name__ == "__main__":
    main()
