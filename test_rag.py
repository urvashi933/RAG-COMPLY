from utils.rag_pipeline import rag_answer

query = "What is the procedure for holding a Board Meeting under the Companies Act 2013?" 
sector = "legal"
result = rag_answer(query, sector)

print("\nANSWER:\n", result["answer"])
print("\nSOURCES:")
for s in result["sources"]:
    print("-", s)
