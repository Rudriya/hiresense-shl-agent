from app.services.retriever import (
    retrieve_assessments
)


def get_recommendations(
    query,
    top_k=10
):

    results = retrieve_assessments(
        query=query,
        top_k=top_k
    )

    formatted = []

    for item in results:

        formatted.append(
            {
                "name": item.get(
                    "name",
                    ""
                ),
                "url": item.get(
                    "url",
                    ""
                ),
                "test_type": item.get(
                    "test_type",
                    []
                )
            }
        )

    return formatted
