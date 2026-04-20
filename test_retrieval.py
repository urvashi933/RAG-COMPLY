from utils.retriever import retrieve_chunks

query = "what's the benefit of startups?"
sector = "legal"

results = retrieve_chunks(query, sector)

for r in results:
    print("\nSOURCE:", r["source"])
    print("TEXT:", r["text"])