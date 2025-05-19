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
        
        # Generate a unique chat ID if not present in conversation history
        chat_id = None
        if not conversation_history:
            chat_id = os.urandom(8).hex()
        else:
            chat_id = conversation_history[0].get('chat_id', os.urandom(8).hex())
        
        # Add current prompt to conversation history with chat ID
        conversation_history.append({"role": "user", "content": prompt, "chat_id": chat_id})
        
        # Create context from conversation history
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
        
        # Generate response with context
        response = model.generate_content(context)
        
        # Store AI response in history with chat ID
        conversation_history.append({"role": "assistant", "content": response.text, "chat_id": chat_id})
        
        # Keep only last 10 messages to manage memory
        if len(conversation_history) > 10:
            conversation_history.pop(0)
            conversation_history.pop(0)
            
        return {"response": response.text, "chat_id": chat_id}
    except Exception as e:
        raise Exception(f"Error generating content: {str(e)}")