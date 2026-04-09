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

def save_index(embeddings, metadata, folder): 
    dim = len(embeddings[0]) 
    index = faiss.IndexFlatL2(dim) 
    index.add(np.array(embeddings).astype('float32')) 
    os.makedirs(folder, exist_ok=True) 
    faiss.write_index(index, f"{folder}/index.faiss") 
    with open(f"{folder}/meta.pkl", 'wb') as f: 
        pickle.dump(metadata, f) 
 
def load_index(folder): 
    index = faiss.read_index(f"{folder}/index.faiss") 
    with open(f"{folder}/meta.pkl", 'rb') as f: 
        meta = pickle.load(f) 
    return index, meta