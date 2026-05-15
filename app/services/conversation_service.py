# app/services/conversation_service.py

import re


def extract_context(messages):
    """
    Extract hiring context from full conversation history.
    """

    full_text = " ".join(
        [m.content for m in messages]
    ).lower()

    context = {
        "role": None,
        "seniority": None,
        "needs_personality": False,
        "needs_cognitive": False,
        "needs_technical": False,
        "needs_leadership": False,
        "needs_communication": False
    }

    # =========================
    # Role Detection
    # =========================

    roles = [
        "java developer",
        "python developer",
        "software engineer",
        "developer",
        "engineer",
        "manager",
        "sales executive",
        "sales",
        "analyst",
        "data analyst",
        "customer service"
    ]

    for role in roles:

        if role in full_text:

            context["role"] = role

            break

    # =========================
    # Seniority Detection
    # =========================

    seniority_levels = [
        "intern",
        "junior",
        "mid-level",
        "mid level",
        "senior",
        "lead",
        "manager"
    ]

    for level in seniority_levels:

        if level in full_text:

            context["seniority"] = level

            break

    # =========================
    # Personality Need
    # =========================

    personality_keywords = [
        "personality",
        "behavior",
        "behavioral",
        "motivation",
        "culture fit"
    ]

    if any(
        word in full_text
        for word in personality_keywords
    ):

        context["needs_personality"] = True

    # =========================
    # Cognitive Need
    # =========================

    cognitive_keywords = [
        "cognitive",
        "aptitude",
        "analytical",
        "problem solving",
        "reasoning"
    ]

    if any(
        word in full_text
        for word in cognitive_keywords
    ):

        context["needs_cognitive"] = True

    # =========================
    # Technical Need
    # =========================

    technical_keywords = [
        "coding",
        "technical",
        "developer",
        "java",
        "python",
        "software",
        "sql"
    ]

    if any(
        word in full_text
        for word in technical_keywords
    ):

        context["needs_technical"] = True

    # =========================
    # Leadership Need
    # =========================

    leadership_keywords = [
        "leadership",
        "manager",
        "stakeholder",
        "team management"
    ]

    if any(
        word in full_text
        for word in leadership_keywords
    ):

        context["needs_leadership"] = True

    # =========================
    # Communication Need
    # =========================

    communication_keywords = [
        "communication",
        "stakeholder",
        "presentation",
        "client-facing"
    ]

    if any(
        word in full_text
        for word in communication_keywords
    ):

        context["needs_communication"] = True

    return context


def needs_clarification(context):
    """
    Decide whether more clarification is needed.
    """

    if not context["role"]:
        return True

    if not context["seniority"]:
        return True

    return False


def generate_clarification_question(context):
    """
    Ask ONE concise clarification question.
    """

    if not context["role"]:

        return (
            "What kind of role are you hiring for?"
        )

    if not context["seniority"]:

        return (
            "What seniority level are you hiring for?"
        )

    return None


def build_search_query(context):
    """
    Convert extracted context into retrieval query.
    """

    query_parts = []

    if context["role"]:
        query_parts.append(context["role"])

    if context["seniority"]:
        query_parts.append(context["seniority"])

    if context["needs_personality"]:
        query_parts.append("personality")

    if context["needs_cognitive"]:
        query_parts.append("cognitive")

    if context["needs_technical"]:
        query_parts.append("technical")

    if context["needs_leadership"]:
        query_parts.append("leadership")

    if context["needs_communication"]:
        query_parts.append("communication")

    return " ".join(query_parts)


# ====================================
# Comparison Query Detection
# ====================================

def is_comparison_query(text):
    """
    Detect comparison intent.
    """

    comparison_words = [
        "compare",
        "difference between",
        "vs",
        "versus"
    ]

    text = text.lower()

    return any(
        word in text
        for word in comparison_words
    )


def extract_comparison_names(text):
    """
    Extract two assessment names from comparison query.
    """

    text = text.lower()

    # remove compare keyword
    text = text.replace("compare", "")

    separators = [
        " vs ",
        " versus ",
        " and "
    ]

    for sep in separators:

        if sep in text:

            parts = text.split(sep)

            if len(parts) >= 2:

                return (
                    parts[0].strip(),
                    parts[1].strip()
                )

    return None, None


# ====================================
# Refinement Query Detection
# ====================================

def is_refinement_query(text):
    """
    Detect refinement/update intent.
    """

    refinement_words = [
        "actually",
        "also",
        "add",
        "include",
        "instead",
        "update"
    ]

    text = text.lower()

    return any(
        word in text
        for word in refinement_words
    )