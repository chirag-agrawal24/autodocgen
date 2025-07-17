import os
import requests
from groq import Groq
from dotenv import  load_dotenv
from autodocgen import GROQ_MODEL
load_dotenv()
client = Groq()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def generate_file_description_ai(code: str, model=GROQ_MODEL) -> str:
    if not GROQ_API_KEY:
        return "No description available (GROQ_API_KEY not set)."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You're an assistant that summarizes Python files."},
            {"role": "user", "content": f"Summarize what this Python file does:\n\n{code}"}
        ],
        "model": model
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", json=data, headers=headers)
    if response.ok:
        return response.json()["choices"][0]["message"]["content"].strip()
    return "AI summary failed."


def generate_docstring(function_name, args, file_context=None, model=GROQ_MODEL):
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


import os
import requests

def generate_readme_with_ai(project_path, file_descriptions,model=GROQ_MODEL ):
    # Prepare basic input for AI
    file_summary = "\n".join(
        f"- {os.path.relpath(path, project_path)}: {desc}"
        for path, desc in file_descriptions.items()
    )

    prompt = f"""
You are a helpful documentation generator. Create a clear, professional, and well-structured README.md for the following project.

Project Description:
This project includes auto-generated documentation for a Python codebase.

Files:
{file_summary}

Include sections:
- Project Overview
- Module Descriptions
- How to Regenerate Documentation (include this command):
  python -m yourdocgen.cli --path . --output-dir docs --fmt html --use-ai --pdf --readme

Format it in markdown.
"""

    # Call Groq API
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
        print(f"❌ Groq AI README generation failed: {e}")
        return ""    
    
