# app/services/comparison_service.py

from app.services.recommendation_engine import (
    get_recommendations
)


def find_assessment_by_name(name):
    """
    Find assessment using:
    1. acronym expansion
    2. semantic retrieval
    3. fuzzy matching
    """

    if not name:

        return None

    name = name.lower().strip()

    # ====================================
    # Acronym Expansion FIRST
    # ====================================

    acronym_map = {
        "opq": (
            "occupational personality questionnaire"
        ),
        "gsa": "general ability",
        "sjt": "situational judgement"
    }

    expanded_query = acronym_map.get(
        name,
        name
    )

    # ====================================
    # Semantic Search
    # ====================================

    results = get_recommendations(
        query=expanded_query,
        top_k=10
    )

    # ====================================
    # Exact / Partial Match
    # ====================================

    for item in results:

        item_name = item["name"].lower()

        if (
            expanded_query in item_name
            or item_name in expanded_query
            or name in item_name
        ):

            return item

    # ====================================
    # Fallback
    # ====================================

    if results:

        return results[0]

    return None


def format_assessment(item):
    """
    Format assessment details.
    """

    if not item:

        return "Assessment not found."

    return f"""
Name: {item.get('name', 'N/A')}

Test Types:
{', '.join(item.get('test_type', []))}

Skills:
{', '.join(item.get('skills', []))}

Duration:
{item.get('duration', 'Not specified')}

URL:
{item.get('url', 'N/A')}
"""


def compare_assessments(name_1, name_2):
    """
    Compare two SHL assessments.
    """

    item_1 = find_assessment_by_name(name_1)

    item_2 = find_assessment_by_name(name_2)

    if not item_1 and not item_2:

        return (
            "I could not find either assessment "
            "in the SHL catalog."
        )

    if not item_1:

        return (
            f"I could not find '{name_1}' "
            "in the SHL catalog."
        )

    if not item_2:

        return (
            f"I could not find '{name_2}' "
            "in the SHL catalog."
        )

    comparison = f"""
Assessment Comparison

==============================

ASSESSMENT 1

{format_assessment(item_1)}

==============================

ASSESSMENT 2

{format_assessment(item_2)}

==============================

Key Differences

- Assessment 1 focuses on:
  {', '.join(item_1.get('skills', []))}

- Assessment 2 focuses on:
  {', '.join(item_2.get('skills', []))}

- Assessment 1 test types:
  {', '.join(item_1.get('test_type', []))}

- Assessment 2 test types:
  {', '.join(item_2.get('test_type', []))}
"""

    return comparison.strip()