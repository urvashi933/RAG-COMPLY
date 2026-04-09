import faiss, pickle, numpy as np, os
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
