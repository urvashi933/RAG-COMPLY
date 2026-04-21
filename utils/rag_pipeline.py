from utils.retriever import retrieve_chunks
from utils.prompt_template import build_prompt
from utils.answer_generator import generate_answer
from utils.logger import log_question, log_unanswered
from utils.query_classifier import is_definition_query


SECTORS=["legal","workforce"]
def rag_answer(query: str, sector: str, user_id: int = None) -> dict:
    """
    Central RAG pipeline function.
    Controls retrieval, generation, validation and logging.
    """

    # 1️⃣ Log every user question (for history & analytics)
    # user_id is required by DB schema; propagate from caller (app route)
    log_question(query, sector, user_id)
    # 2️⃣ Retrieve relevant document chunks using FAISS
    retrieved_chunks = retrieve_chunks(query, sector)
    print("DEBUG -> retrieved_chunks:", retrieved_chunks)
    print("DEBUG -> type:", type(retrieved_chunks))
    print("DEBUG -> length:", len(retrieved_chunks) if retrieved_chunks is not None else "None")

    used_sector = sector
    # 3️⃣ If not found, try other sectors
    if not retrieved_chunks:
        for other_sector in SECTORS:
            if other_sector != sector:
                retrieved_chunks = retrieve_chunks(query, other_sector)
                if retrieved_chunks:
                    used_sector = other_sector
                    break

    # 4️⃣ Still nothing → handle definition / unanswered

    if not retrieved_chunks:
        if is_definition_query(query):
            prompt = build_prompt([], query)
            answer = generate_answer(prompt)
            return {
                "answer": answer,
                "sources": []
            }

        log_unanswered(query, sector)
       # print("hi")
        return {
            "answer": "Answer not found in the provided documents.",
            "sources": []
        }


    # 5️⃣ Build strict RAG prompt using retrieved chunks
    prompt = build_prompt(retrieved_chunks, query)

    # 6️⃣ Generate answer using Gemini (2.5 Flash-Lite)
    answer = generate_answer(prompt)

    # 7️⃣ Collect unique document sources for citation
    sources = list(
        set(chunk["source"] for chunk in retrieved_chunks)
    )

    # 8️⃣ Return final response
    return {
        "answer": answer,
        "sources": sources,
        "sector_used": used_sector
    }