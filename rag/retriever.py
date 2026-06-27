"""
Hybrid Retriever

Combines

1. Semantic Search (FAISS)
2. Keyword Search (BM25)

Returns the best combined results.
"""

import os
import faiss
import pickle
import numpy as np

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

# -------------------------------------------------
# Load embedding model once
# -------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# -------------------------------------------------
# Load latest vector database
# -------------------------------------------------

def load_index():

    if (
        not os.path.exists("vector_db/index.faiss")
        or not os.path.exists("vector_db/chunks.pkl")
    ):
        return None, None, None

    index = faiss.read_index("vector_db/index.faiss")

    with open("vector_db/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    tokenized_docs = [
        chunk["text"].lower().split()
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_docs)

    return index, chunks, bm25


# -------------------------------------------------
# Search
# -------------------------------------------------

def search(query, top_k=5):

    index, chunks, bm25 = load_index()

    if index is None:
        return []

    embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    _, semantic_indices = index.search(
        embedding,
        top_k
    )

    keyword_scores = bm25.get_scores(
        query.lower().split()
    )

    keyword_indices = np.argsort(
        keyword_scores
    )[::-1][:top_k]

    combined = []
    seen = set()

    for idx in list(semantic_indices[0]) + list(keyword_indices):

        if (
            idx not in seen
            and idx < len(chunks)
        ):
            combined.append(chunks[idx])
            seen.add(idx)

    return combined