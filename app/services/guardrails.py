# app/services/guardrails.py

import re


# ====================================
# Blocked Topics
# ====================================

BLOCKED_TOPICS = [
    "legal advice",
    "salary negotiation",
    "firing employees",
    "politics",
    "religion",
    "medical advice",
    "financial advice"
]


# ====================================
# Prompt Injection Patterns
# ====================================

PROMPT_INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all instructions",
    r"reveal system prompt",
    r"show system prompt",
    r"display hidden prompt",
    r"bypass restrictions",
    r"jailbreak",
    r"developer message",
    r"pretend to be",
    r"act as",
    r"you are now",
    r"simulate",
    r"disable guardrails"
]


# ====================================
# Off-topic Queries
# ====================================

OFF_TOPIC_PATTERNS = [
    r"how to hire",
    r"best hiring strategy",
    r"interview questions",
    r"how should i fire",
    r"fire employees",
    r"employee termination",
    r"labor law",
    r"resume review",
    r"salary negotiation"
]


def contains_blocked_topic(text):
    """
    Detect blocked topics.
    """

    text = text.lower()

    return any(
        topic in text
        for topic in BLOCKED_TOPICS
    )


def detect_prompt_injection(text):
    """
    Detect prompt injection attempts.
    """

    text = text.lower()

    for pattern in PROMPT_INJECTION_PATTERNS:

        if re.search(pattern, text):

            return True

    return False


def detect_off_topic_query(text):
    """
    Detect non-SHL hiring queries.
    """

    text = text.lower()

    for pattern in OFF_TOPIC_PATTERNS:

        if re.search(pattern, text.lower()):

            return True

    return False


def is_blocked_query(text):
    """
    Main guardrail router.
    """

    if contains_blocked_topic(text):

        return True

    if detect_prompt_injection(text):

        return True

    if detect_off_topic_query(text):

        return True

    return False