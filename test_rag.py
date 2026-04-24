from utils.rag_pipeline import rag_answer

query = "What are the legal requirements for the composition of an Internal Committee (IC), and why must at least one member be an external person from an NGO or an association committed to the cause of women?" 
sector = "workforce"
result = rag_answer(query, sector)

print("\nANSWER:\n", result["answer"])
print("\nSOURCES:")
for s in result["sources"]:
    print("-", s)
