from app.services.recommendation_engine import get_recommendations

query = "java developer personality communication"

results = get_recommendations(query)

for r in results:

    print("\n===================")

    print("NAME:", r["name"])

    print("SCORE:", r["final_score"])

    print("TYPE:", r["test_type"])