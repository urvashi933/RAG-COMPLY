import faiss # extension for efficient similarity search
import numpy as np
import os
import pickle

def build_faiss_index(embeddings, metadatas, save_path):
    dimension = len(embeddings[0]) # 384 for MiniLM embeddings
    index = faiss.IndexFlatL2(dimension)# L2 distance for similarity search that means lower distance = more similar 
    # indexflatl2 is a simple index that computes L2 distance between vectors, suitable for small to medium datasets. 
    # For larger datasets, consider using more complex indexes like IndexIVFFlat or IndexHNSWFlat for faster search at the cost of some accuracy.
    # l2 distance is the square root of the sum of squared differences between two vectors. It measures how far apart two vectors are in the embedding space. A smaller L2 distance indicates that the vectors are more similar, while a larger distance indicates they are less similar. In the context of similarity search, we want to find vectors that have a small L2 distance to the query vector, as this suggests they are semantically similar.

    vectors = np.array(embeddings).astype("float32") # Convert to float32 for Faiss
    index.add(vectors)
    os.makedirs(save_path, exist_ok=True)

    faiss.write_index(index, os.path.join(save_path, "index.faiss"))

    with open(os.path.join(save_path, "metadata.pkl"), "wb") as f: # Save metadata for retrieval
        pickle.dump(metadatas, f) # dumping a list of dicts, each dict has keys: sector, document, chunk_id, source, text
