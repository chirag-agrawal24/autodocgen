import os
import requests
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
HEADERS = {'Authorization': f'Bearer {GROQ_API_KEY}', 'Content-Type':
    'application/json'}


def generate_file_description_ai(code: str, model=
    'meta-llama/llama-4-scout-17b-16e-instruct') ->str:
    """Generate a concise summary of the code using the provided AI model when the initial AI summary attempt fails. 
        Args:
            code (str): The code to be summarized.
            model: The AI model used for generating the summary. 
        Returns: 
            A string describing the provided code."""
    if not GROQ_API_KEY:
        return 'No description available (GROQ_API_KEY not set).'
    headers = {'Authorization': f'Bearer {GROQ_API_KEY}', 'Content-Type':
        'application/json'}
    data = {'messages': [{'role': 'system', 'content':
        "You're an assistant that summarizes Python files."}, {'role':
        'user', 'content':
        f"""Summarize what this Python file does:

{code}"""}], 'model': model}
    response = requests.post('https://api.groq.com/openai/v1/chat/completions',
        json=data, headers=headers)
    if response.ok:
        return response.json()['choices'][0]['message']['content'].strip()
    return 'AI summary failed.'


def generate_docstring(function_name, args, file_context=None, model=
    'meta-llama/llama-4-scout-17b-16e-instruct'):
    """Generate a docstring for a given function based on its name, arguments, file context, and model.

### Parameters

* function_name (str): The name of the function to generate a docstring for.
* args (list): A list of arguments the function takes.
* file_context (str): The context of the file the function is in.
* model (object): The model used to generate the docstring.

### Returns

* str: A generated docstring for the specified function."""
    prompt = f"""
Generate a concise, readable Python docstring for the following function:

Function: {function_name}
Arguments: {', '.join(args)}

{f'Context:{file_context[:300]}' if file_context else ''}
Respond with only the docstring content (no quotes or formatting).
"""
    try:
        completion = client.chat.completions.create(model=model, messages=[
            {'role': 'user', 'content': prompt}], temperature=1,
            max_completion_tokens=1024, top_p=1, stream=False, stop=None)
        response_str = completion.choices[0].message.content or ''
        return response_str.strip()
    except Exception as e:
        print(f'❌ Groq AI docstring generation failed: {e}')
        return None


import os
import requests


def generate_readme_with_ai(project_path, file_descriptions, model=
    'meta-llama/llama-4-scout-17b-16e-instruct'):
    """Generate a README file for a project using AI insights.

 Args:
  project_path (str): The path to the project directory.
  file_descriptions (dict): A dictionary of file descriptions.
  model: The AI model used to generate the README summary.

 Returns:
  None 

 Raises:
  Exception: If AI summary fails."""
    file_summary = '\n'.join(
        f'- {os.path.relpath(path, project_path)}: {desc}' for path, desc in
        file_descriptions.items())
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
    try:
        completion = client.chat.completions.create(model=model, messages=[
            {'role': 'user', 'content': prompt}], temperature=1,
            max_completion_tokens=1024, top_p=1, stream=False, stop=None)
        response_str = completion.choices[0].message.content or ''
        return response_str.strip()
    except Exception as e:
        print(f'❌ Groq AI README generation failed: {e}')
        return ''
