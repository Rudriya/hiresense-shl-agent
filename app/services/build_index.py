import json
import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


CATALOG_PATH = "app/data/catalog.json"

INDEX_PATH = "app/data/faiss_index/shl.index"

METADATA_PATH = "app/data/faiss_index/metadata.pkl"


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def load_catalog():

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:

        return json.load(f)


def create_document(assessment):

    return f"""
    Name: {assessment.get('name', '')}

    Description:
    {assessment.get('description', '')}

    Skills:
    {' '.join(assessment.get('skills', []))}

    Test Type:
    {' '.join(assessment.get('test_type', []))}

    Duration:
    {assessment.get('duration', '')}
    """


def build_index():

    catalog = load_catalog()

    documents = []

    metadata = []

    for item in catalog:

        doc = create_document(item)

        documents.append(doc)

        metadata.append(item)

    print(f"Creating embeddings for {len(documents)} assessments...")

    embeddings = model.encode(
        documents,
        show_progress_bar=True
    )

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "wb") as f:

        pickle.dump(metadata, f)

    print("\nFAISS index created successfully!")

    print(f"Saved index to: {INDEX_PATH}")

    print(f"Saved metadata to: {METADATA_PATH}")


if __name__ == "__main__":

    build_index()