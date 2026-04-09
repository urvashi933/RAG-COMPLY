from google import genai
from sqlalchemy import text
from config import GEMINI_API_KEY, EMBEDDING_MODEL
client = genai.Client(api_key=GEMINI_API_KEY)
def get_embedding(text):
# This converts text into a 768-dimension vector
    result = client.models.embed_content(
    model=EMBEDDING_MODEL,
    contents=text
    )
    return result.embeddings[0].values
