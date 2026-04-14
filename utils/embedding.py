from sentence_transformers import SentenceTransformer
from config import GEMINI_API_KEY, EMBEDDING_MODEL

model= SentenceTransformer(EMBEDDING_MODEL)

def get_embedding(text:str):
# This converts text into a 768-dimension vector
    """
    Generate embeddings for text using SentenceTrasformer.
    """
    embedding=model.encode(text)
    return embedding.tolist()
