from google import genai 
from config import GEMINI_API_KEY, GENERATIVE_MODEL 
 
client = genai.Client(api_key=GEMINI_API_KEY) 
 
def generate_answer(prompt): 
    response = client.models.generate_content( 
        model=GENERATIVE_MODEL, 
        contents=prompt 
    ) 
    return response.text.strip() 