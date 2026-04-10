def build_prompt(context_chunks, query): 
    context_text = "" 
    for i, chunk in enumerate(context_chunks, start=1): 
        context_text += f"\nSOURCE {i}:\n{chunk['text']}\n" 
 
    prompt = f""" 
    You are a professional Startup Incubator Consultant. 
     
    CONTEXT (Use this data only): 
    {context_text} 
 
    USER QUESTION: {query} 
     
    INSTRUCTIONS: 
    - If the answer is in the context, explain it clearly with references to source numbers. 
    - If the answer is NOT in the context, say "I'm sorry, my current training documents do 
not contain this information." 
    """ 
    return prompt 