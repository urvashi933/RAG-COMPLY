from utils.rag_pipeline import rag_answer

query = "what's the benefit of startups?" 
<<<<<<< HEAD
sector = "workforce"
=======


sector = "legal"
>>>>>>> d110fddc4f9f22f5b77596f7ff5a36c3bf22f239

result = rag_answer(query, sector)

print("\nANSWER:\n", result["answer"])
print("\nSOURCES:")
for s in result["sources"]:
    print("-", s)
