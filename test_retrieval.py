from utils.retriever import retrieve_chunks

query = "What is contract drafting?"
sector = "legal"

results = retrieve_chunks(query, sector)

for r in results:
    print("\nSOURCE:", r["source"])
    print("TEXT:", r["text"])