def build_prompt(context_chunks, query): 
    context_text = "" 

    for i, chunk in enumerate(context_chunks, start=1): 
        context_text += f"\nSOURCE {i}:\n{chunk['text']}\n" 
 
    prompt = f""" 
    You are a domain-specific consultancy assistant.

    RULES(STRICT):
    1. If the user asks for the MEANING or DEFINITION of a word or term present in document only:
        - You MAY explain it in simple language.
        - Prefer explanantions consistent with the domain context.
    2. For advisory,legal, procedural, or factual question:
        - Answer ONLY using the information in the sources below.
    3. Do NOT invent legal rules,policies or procedures.
    4. If the answer cannot be derived from sources and is not a definition:
       reply exactly:
       "Answer not found in the provided documents."
     
    CONTEXT (Use this data only): 
    {context_text} 
 
    USER QUESTION: {query} 
     
    INSTRUCTIONS: 
    - If the answer is in the context, explain it clearly with references to source numbers. 
    - If the answer is NOT in the context, say "I'm sorry, my current training documents do 
    not contain this information." 

    ANSWER:
    """ 

    return prompt 