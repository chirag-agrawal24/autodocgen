import os
import requests
from groq import Groq
from dotenv import  load_dotenv

load_dotenv()
client = Groq()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def generate_docstring(function_name, args, file_context=None, model="meta-llama/llama-4-scout-17b-16e-instruct"):
    prompt = f"""
Generate a concise, readable Python docstring for the following function:

Function: {function_name}
Arguments: {', '.join(args)}

{f'Context:{file_context[:300]}' if file_context else ''}
Respond with only the docstring content (no quotes or formatting).
"""

    
    try:
        completion = client.chat.completions.create(
        model=model,
        messages=[
        {
            "role": "user",
            "content": prompt
        }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
        )

        response_str = completion.choices[0].message.content or ""

        
        return response_str.strip()
    except Exception as e:
        print(f"❌ Groq AI docstring generation failed: {e}")
        return None
