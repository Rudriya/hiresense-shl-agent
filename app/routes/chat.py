# app/routes/chat.py

from fastapi import APIRouter

from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    Recommendation
)

from app.services.guardrails import (
    is_blocked_query
)

from app.services.conversation_service import (
    extract_context,
    needs_clarification,
    generate_clarification_question,
    build_search_query,
    is_comparison_query,
    extract_comparison_names
)

from app.services.recommendation_engine import (
    get_recommendations
)

from app.services.comparison_service import (
    compare_assessments
)

from app.services.llm_service import (
    generate_reply
)


router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    # ====================================
    # Latest User Message
    # ====================================

    latest_message = (
        request.messages[-1].content
    )

    # ====================================
    # Guardrails
    # ====================================

    if is_blocked_query(latest_message):

        return ChatResponse(
            reply=(
                "I can only help with SHL "
                "assessment recommendations, "
                "refinements, and comparisons."
            ),
            recommendations=[],
            end_of_conversation=False
        )

    # ====================================
    # Comparison Handling
    # ====================================

    if is_comparison_query(latest_message):

        name_1, name_2 = (
            extract_comparison_names(
                latest_message
            )
        )

        if not name_1 or not name_2:

            return ChatResponse(
                reply=(
                    "Please specify the two "
                    "assessments you want "
                    "to compare."
                ),
                recommendations=[],
                end_of_conversation=False
            )

        comparison = compare_assessments(
            name_1,
            name_2
        )

        return ChatResponse(
            reply=comparison,
            recommendations=[],
            end_of_conversation=True
        )

    # ====================================
    # Extract Context
    # ====================================

    context = extract_context(
        request.messages
    )

    # ====================================
    # Clarification Handling
    # ====================================

    if needs_clarification(context):

        question = (
            generate_clarification_question(
                context
            )
        )

        return ChatResponse(
            reply=question,
            recommendations=[],
            end_of_conversation=False
        )

    # ====================================
    # Build Search Query
    # ====================================

    query = build_search_query(
        context
    )

    # ====================================
    # Retrieve Recommendations
    # ====================================

    results = get_recommendations(
        query=query,
        top_k=10
    )

    # ====================================
    # Empty Recommendation Handling
    # ====================================

    if not results:

        return ChatResponse(
            reply=(
                "I could not find suitable "
                "SHL assessments for the "
                "provided requirements."
            ),
            recommendations=[],
            end_of_conversation=True
        )

    # ====================================
    # Format Recommendations
    # ====================================

    recommendations = []

    for item in results:

        recommendations.append(
            Recommendation(
                name=item.get("name", ""),
                url=item.get("url", ""),
                test_type=item.get(
                    "test_type",
                    []
                )
            )
        )

    # ====================================
    # Generate Grounded Reply
    # ====================================

    reply = generate_reply(results)

    # ====================================
    # Final Response
    # ====================================

    return ChatResponse(
        reply=reply,
        recommendations=recommendations,
        end_of_conversation=True
    )