"""
embeddings.py

Creates embeddings for document chunks
and stores them in a FAISS vector database.
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_vector_store(chunks):
    """
    Convert text chunks into embeddings and
    save them in FAISS.
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    os.makedirs("vector_db", exist_ok=True)

    faiss.write_index(index, "vector_db/index.faiss")

    with open("vector_db/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    return index