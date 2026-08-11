"""Prompt Library - Simple email templates."""

TEMPLATES = {
    "welcome": {
        "name": "Welcome Email",
        "prompt": "Write a welcome email for {recipient_name} joining {company_name}. Format as:\nSubject: <subject>\nBody:\n<body>",
    },
    "followup": {
        "name": "Follow-up Email",
        "prompt": "Write a follow-up email to {recipient_name} about {topic}. Format as:\nSubject: <subject>\nBody:\n<body>",
    },
    "meeting": {
        "name": "Meeting Request",
        "prompt": "Write a meeting request email to {recipient_name} for {purpose} on {date}. Format as:\nSubject: <subject>\nBody:\n<body>",
    },
    "support": {
        "name": "Customer Support",
        "prompt": "Write a support reply to {customer_name} about {issue}. Format as:\nSubject: <subject>\nBody:\n<body>",
    },
    "feedback": {
        "name": "Feedback Request",
        "prompt": "Write an email to {customer_name} requesting feedback regarding {product_or_service}. Format as:\nSubject: <subject>\nBody:\n<body>",
    },
    "outreach": {
        "name": "Sales Outreach",
        "prompt": "Write a cold sales outreach email to {prospect_name} at {company_name} introducing {solution_name}. Format as:\nSubject: <subject>\nBody:\n<body>",
    },
    "thank_you": {
        "name": "Thank You Email",
        "prompt": "Write a sincere thank you email to {recipient_name} for {reason}. Format as:\nSubject: <subject>\nBody:\n<body>",
    },
    "announcement": {
        "name": "Product Announcement",
        "prompt": "Write an announcement email to {audience_name} introducing {new_feature_or_product}. Format as:\nSubject: <subject>\nBody:\n<body>",
    },
}


def get_template(template_id):
    """Get a template by ID or case-insensitive key. Returns None if not found."""
    if not template_id:
        return None
    tid_lower = str(template_id).strip().lower()
    return TEMPLATES.get(tid_lower)


def list_templates():
    """Return list of (id, name) pairs."""
    return [(tid, t["name"]) for tid, t in TEMPLATES.items()]
