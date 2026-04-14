from utils.rag_pipeline import rag_answer

query = "what is contract drafting ?"

sector = "workforce"

result = rag_answer(query, sector)

print("\nANSWER:\n", result["answer"])
print("\nSOURCES:")
for s in result["sources"]:
    print("-", s)
