from utils.retriever import retrieve_chunks

query = "What is the procedure for holding a Board Meeting under the Companies Act 2013?"
sector = "legal"

results = retrieve_chunks(query, sector)

for r in results:
    print("\nSOURCE:", r["source"])
    print("TEXT:", r["text"])