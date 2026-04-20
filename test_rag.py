from utils.rag_pipeline import rag_answer

query = "what's the benefit of startups?" 


sector = "legal"

result = rag_answer(query, sector)

print("\nANSWER:\n", result["answer"])
print("\nSOURCES:")
for s in result["sources"]:
    print("-", s)
