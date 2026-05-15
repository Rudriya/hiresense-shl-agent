import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


INDEX_PATH = "app/data/faiss_index/shl.index"
METADATA_PATH = "app/data/faiss_index/metadata.pkl"


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

index = faiss.read_index(INDEX_PATH)

with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)


def semantic_search(query, top_k=20):

    query_embedding = model.encode([query])

    query_embedding = np.array(
        query_embedding,
        dtype=np.float32
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        if idx < len(metadata):

            item = metadata[idx].copy()

            item["semantic_score"] = float(distance)

            results.append(item)

    return results