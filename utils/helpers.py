"""
Helper utilities for Mind Palace application.
Uses modern Google GenAI SDK for all API calls.
"""
import json
import os
from PyPDF2 import PdfReader
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Unified client for all Gemini API calls (modern SDK)
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

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

def call_gemini(prompt_config, context_text="", target_text="", **kwargs):
    """
    Call Gemini API for standard text generation using the modern SDK.
    
    Args:
        prompt_config (dict): Dictionary with 'system_instruction' and 'user_instruction'
        context_text (str): The main content/document text to process
        target_text (str): Target topic, concept, or specific text (used in formatting)
        **kwargs: Additional variables to format the user_instruction
    
    Returns:
        str: Generated text response from Gemini
    """
    model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
    
    # Format user instruction with provided variables
    format_vars = {'target_text': target_text, **kwargs}
    user_instruction = prompt_config['user_instruction'].format(**format_vars)
    
    # Build final prompt with clear structure
    if context_text:
        full_prompt = f"{user_instruction}\n\nCONTENT:\n{context_text}"
    else:
        full_prompt = user_instruction
    
    # Get system instruction (optional)
    system_instruction = prompt_config.get('system_instruction', '')
    
    # Call Gemini with modern SDK
    response = client.models.generate_content(
        model=model_name,
        contents=full_prompt,
        config={
            "system_instruction": system_instruction
        } if system_instruction else {}
    )
    
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


def call_gemini_structured(prompt_text, schema_class, model_name="gemini-2.0-flash"):
    """
    Call Gemini API with structured output using Pydantic schema.
    
    Args:
        prompt_text (str): The prompt to send to Gemini
        schema_class: Pydantic BaseModel class defining the expected structure
        model_name (str): Gemini model to use (default: gemini-2.0-flash-exp)
    
    Returns:
        Instance of schema_class with validated data
    
    Example:
        from pydantic import BaseModel
        class Recipe(BaseModel):
            name: str
            ingredients: list[str]
        
        result = call_gemini_structured("Extract recipe...", Recipe)
    """
    response = client.models.generate_content(
        model=model_name,
        contents=prompt_text,
        config={
            "response_mime_type": "application/json",
            "response_schema": schema_class,
        },
    )
    
    # Validate and return as Pydantic model instance
    return schema_class.model_validate_json(response.text)
