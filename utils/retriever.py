import faiss
import pickle
import os
import numpy as np
from utils.embedding import get_embedding


SIMILARITY_THRESHOLD = 0.75  # tune if needed


def load_faiss_index(sector):
    index_path = f"vector_store/{sector}_faiss"
    index = faiss.read_index(os.path.join(index_path, "index.faiss"))

    with open(os.path.join(index_path, "metadata.pkl"), "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


def retrieve_chunks(query, sector, top_k=3):
    index, metadata = load_faiss_index(sector)

    query_embedding = np.array([get_embedding(query)]).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    # 🔴 TEMP DEBUG PRINTS (HERE ONLY)
    print("DEBUG distances:", distances)
    print("DEBUG indices:", indices)

    results = []

    # 🔥 THRESHOLD FILTER HERE 🔥
    for score, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        # IMPORTANT: Check index type
        if score <= SIMILARITY_THRESHOLD:
            results.append(metadata[idx])

    return results