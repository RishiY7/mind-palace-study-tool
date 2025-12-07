"""
Helper utilities for Mind Palace application.
"""
import json
import os
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def load_prompt(prompt_file):
    """Load a prompt configuration from JSON file."""
    prompt_path = os.path.join('prompts', prompt_file)
    with open(prompt_path, 'r') as f:
        return json.load(f)

def extract_text_from_pdf(pdf_file):
    """Extract text content from a PDF file."""
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def call_gemini(prompt_config, user_text, **kwargs):
    """
    Call Gemini API with the given prompt configuration.
    
    Args:
        prompt_config: Dictionary with system_instruction and user_instruction
        user_text: The main text content to process
        **kwargs: Additional variables to format the user_instruction
    """
    model = genai.GenerativeModel(
        model_name=os.getenv('GEMINI_MODEL', 'gemini-flash-lite-latest'),
        system_instruction=prompt_config['system_instruction']
    )
    
    # Format user instruction with any provided variables
    user_instruction = prompt_config['user_instruction'].format(**kwargs) if kwargs else prompt_config['user_instruction']
    
    # Combine instruction with text
    full_prompt = f"{user_instruction}\n\n{user_text}"
    
    response = model.generate_content(full_prompt)
    return response.text

def parse_json_response(response_text):
    """
    Extract and parse JSON from Gemini response.
    Handles cases where JSON is wrapped in markdown code blocks.
    """
    # Try to extract JSON from markdown code blocks
    if '```json' in response_text:
        start = response_text.find('```json') + 7
        end = response_text.find('```', start)
        json_text = response_text[start:end].strip()
    elif '```' in response_text:
        start = response_text.find('```') + 3
        end = response_text.find('```', start)
        json_text = response_text[start:end].strip()
    else:
        json_text = response_text.strip()
    
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        # If parsing fails, return the raw text
        return response_text

def chunk_text(text, max_length=5000):
    """Split text into chunks for processing."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_length += len(word) + 1
        if current_length > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks
