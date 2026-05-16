import json
from pathlib import Path

import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)


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

INDEX_PATH = (
    BASE_DIR
    / "data"
    / "faiss_index"
    / "index.faiss"
)


# ====================================
# GLOBALS
# ====================================

_model = None
_index = None
_catalog = None


# ====================================
# LAZY LOAD MODEL
# ====================================

def get_model():

    global _model

    if _model is None:

        _model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return _model


# ====================================
# LAZY LOAD INDEX
# ====================================

def get_index():

    global _index

    if _index is None:

        _index = faiss.read_index(
            str(INDEX_PATH)
        )

    return _index


# ====================================
# LOAD CATALOG
# ====================================

def get_catalog():

    global _catalog

    if _catalog is None:

        with open(
            CATALOG_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            _catalog = json.load(f)

    return _catalog


# ====================================
# RETRIEVAL
# ====================================

def retrieve_assessments(
    query,
    top_k=10
):

    model = get_model()

    index = get_index()

    catalog = get_catalog()

    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        if (
            idx >= 0
            and idx < len(catalog)
        ):

            results.append(
                catalog[idx]
            )

    return results
