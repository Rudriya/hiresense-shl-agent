# app/services/recommendation_engine.py

from app.services.retriever import (
    semantic_search
)


TEST_TYPE_MAP = {
    "P": "Personality",
    "C": "Cognitive",
    "T": "Technical",
    "S": "Simulation"
}


def keyword_overlap_score(query, text):

    query_words = set(
        query.lower().split()
    )

    text_words = set(
        text.lower().split()
    )

    overlap = query_words.intersection(
        text_words
    )

    return len(overlap)


def skill_match_score(query, skills):

    score = 0

    query = query.lower()

    for skill in skills:

        if skill.lower() in query:

            score += 3

    return score


def test_type_boost(query, test_types):

    score = 0

    query = query.lower()

    # Personality boost
    if (
        any(word in query for word in [
            "personality",
            "behavior",
            "culture"
        ])
        and "P" in test_types
    ):

        score += 5

    # Technical boost
    if (
        any(word in query for word in [
            "coding",
            "developer",
            "technical",
            "java",
            "python",
            "sql"
        ])
        and "T" in test_types
    ):

        score += 5

    # Cognitive boost
    if (
        any(word in query for word in [
            "cognitive",
            "aptitude",
            "analytical",
            "reasoning"
        ])
        and "C" in test_types
    ):

        score += 5

    # Simulation boost
    if (
        any(word in query for word in [
            "simulation",
            "scenario",
            "situational"
        ])
        and "S" in test_types
    ):

        score += 5

    return score


def rerank_results(query, candidates):

    ranked = []

    for item in candidates:

        semantic_score = (
            1 / (1 + item["semantic_score"])
        )

        keyword_score = keyword_overlap_score(
            query,
            item.get("description", "")
        )

        skill_score = skill_match_score(
            query,
            item.get("skills", [])
        )

        type_score = test_type_boost(
            query,
            item.get("test_type", [])
        )

        final_score = (
            semantic_score * 2
            + keyword_score * 2
            + skill_score * 3
            + type_score * 4
        )

        item["final_score"] = final_score

        ranked.append(item)

    # ====================================
    # Sort by Best Score
    # ====================================

    ranked.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    # ====================================
    # Filter Weak Results
    # ====================================

    filtered = []

    for item in ranked:

        if item["final_score"] > 3:

            filtered.append(item)

    # ====================================
    # Remove Duplicates
    # ====================================

    unique_results = []

    seen = set()

    for item in filtered:

        name = item["name"]

        if name not in seen:

            unique_results.append(item)

            seen.add(name)

    return unique_results


def get_recommendations(
    query,
    top_k=10
):

    candidates = semantic_search(
        query,
        top_k=25
    )

    ranked = rerank_results(
        query,
        candidates
    )

    return ranked[:top_k]