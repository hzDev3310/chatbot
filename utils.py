import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict

# Load environment variables
load_dotenv()

# Store conversation history
conversation_history: List[Dict[str, str]] = []

# Initialize Gemini client
def init_gemini_client():
    api_key = os.getenv('apiKey')
    if not api_key:
        raise ValueError("API key not found in environment variables")
    
    genai.configure(api_key=api_key)
    return genai

# Generate content using Gemini model
def generate_content(prompt, model="gemini-2.0-flash"):
    try:
        genai_client = init_gemini_client()
        model = genai_client.GenerativeModel(model)
        
        # Add current prompt to conversation history
        conversation_history.append({"role": "user", "content": prompt})
        
        # Create context from conversation history
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
        
        # Generate response with context
        response = model.generate_content(context)
        
        # Store AI response in history
        conversation_history.append({"role": "assistant", "content": response.text})
        
        # Keep only last 10 messages to manage memory
        if len(conversation_history) > 10:
            conversation_history.pop(0)
            conversation_history.pop(0)
            
        return response.text
    except Exception as e:
        raise Exception(f"Error generating content: {str(e)}")