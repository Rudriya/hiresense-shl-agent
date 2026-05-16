import json
from pathlib import Path


# ====================================
# PATHS
# ====================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

CATALOG_PATH = (
    BASE_DIR / "data" / "catalog.json"
)


# ====================================
# LOAD CATALOG
# ====================================

with open(
    CATALOG_PATH,
    "r",
    encoding="utf-8"
) as f:

    catalog = json.load(f)


# ====================================
# SCORING
# ====================================

def score_assessment(
    assessment,
    query
):

    query = query.lower()

    score = 0

    # =========================
    # Name Match
    # =========================

    name = assessment.get(
        "name",
        ""
    ).lower()

    if name in query:

        score += 10

    # =========================
    # Skills Match
    # =========================

    skills = assessment.get(
        "skills",
        []
    )

    for skill in skills:

        if skill.lower() in query:

            score += 5

    # =========================
    # Description Match
    # =========================

    description = assessment.get(
        "description",
        ""
    ).lower()

    for word in query.split():

        if word in description:

            score += 1

    # =========================
    # Test Type Boost
    # =========================

    if "personality" in query:

        if "P" in assessment.get(
            "test_type",
            []
        ):

            score += 5

    if "cognitive" in query:

        if "C" in assessment.get(
            "test_type",
            []
        ):

            score += 5

    if (
        "technical" in query
        or "coding" in query
    ):

        if "T" in assessment.get(
            "test_type",
            []
        ):

            score += 5

    return score


# ====================================
# RETRIEVAL
# ====================================

def retrieve_assessments(
    query,
    top_k=10
):

    scored_results = []

    for assessment in catalog:

        score = score_assessment(
            assessment,
            query
        )

        scored_results.append(
            (
                score,
                assessment
            )
        )

    scored_results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    recommendations = [
        item
        for score, item
        in scored_results[:top_k]
    ]

    return recommendations
