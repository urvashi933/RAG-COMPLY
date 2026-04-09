from utils.retriever import retrieve_top_chunks
from google import genai
from config import GEMINI_API_KEY, GENERATIVE_MODEL
client = genai.Client(api_key=GEMINI_API_KEY)
def multi_agent_rag(query, sector):
	print(f" [Agent 1: Classifier] Analyzing query: {query}")
	print(f" [Agent 2: Researcher] Searching {sector} documents...")
	context_chunks = retrieve_top_chunks(query, sector)
	if not context_chunks:
		print(" [Agent 2] No data found.")
		return {"answer": "No relevant info found in documents.", "sources": []}
	print(f" [Agent 3: Synthesis] Grounding answer in {len(context_chunks)} sources...")
	context_text = "\n".join([c['text'] for c in context_chunks])
	prompt = f"""
SYSTEM ROLE: You are an expert Startup Consultant.
CONTEXT FROM DOCUMENTS: {context_text}
USER QUESTION: {query}
STRICT RULES:
1. Answer ONLY using the context.
2. Be professional and detailed.
3. If not in documents, say: "I details requested are not in my current training
documents."
"""
	response = client.models.generate_content(model=GENERATIVE_MODEL,
											 contents=prompt)
	sources = list(set([c['source'] for c in context_chunks]))
	return {"answer": response.text, "sources": sources}