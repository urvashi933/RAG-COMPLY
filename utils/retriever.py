from utils.embedding import get_embedding
from utils.faiss_indexer import load_index
import numpy as np
def retrieve_top_chunks(query, sector, k=4):
	try:
		index, meta = load_index(f"vector_store/{sector}")
		q_vec = np.array([get_embedding(query)]).astype('float32')
		dist, idxs = index.search(q_vec, k)
		results = []
		for i, idx in enumerate(idxs[0]):
			if idx != -1 and dist[0][i] < 0.8: # Similarity Threshold
				results.append(meta[idx])
		return results
	except:
		return []