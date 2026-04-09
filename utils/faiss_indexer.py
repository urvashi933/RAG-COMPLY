import faiss
import numpy as np
import os
import pickle

def build_faiss_index(embeddings, metadatas, save_path):
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)

    vectors = np.array(embeddings).astype("float32")
    index.add(vectors)
    os.makedirs(save_path, exist_ok=True)

    faiss.write_index(index, os.path.join(save_path, "index.faiss"))

    with open(os.path.join(save_path, "metadata.pkl"), "wb") as f:
        pickle.dump(metadatas, f)