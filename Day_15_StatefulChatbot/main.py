# Import required system modules
import os  # For accessing environment variables
import chainlit as cl  # Import Chainlit for chat interface
import google.generativeai as genai  # Import Google's Generative AI library
from dotenv import load_dotenv  # For loading environment variables from .env file
from typing import Dict, Optional  # For type hints

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure the Gemini AI with the API key
genai.configure(api_key=gemini_api_key)

# Initialize the Gemini model with specified version
model = genai.GenerativeModel('gemini-2.0-flash') # Using Gemini's flash model for faster responses

# OAuth callback decorator for handling authentication
@cl.oauth_callback
def oauth_callback (
    provider_id: str, # ID of the OAuth provider (GitHub)
    token: str,  # Authentication token
    raw_user_data: Dict[str, str],  # User data from OAuth provider
    default_user: cl.User,  # Default user object
) -> Optional[cl.User]:  # Return type annotation
    """
    Handle the OAuth callback from GitHub
    Return the user object if authentication is successful, otherwise None
    """
    print(f"Provider ID: {provider_id}")  # Log the provider ID
    print(f"User data: {raw_user_data}")  # Log the user data
    return default_user  # Return the default user object

# Decorator for chat start event
@cl.on_chat_start
async def handle_chat_start():
    """
    Handle the chat start event
    """
    # Initialize empty history in user session
    cl.user_session.set("history", [])

    # Send welcome message to user
    await cl.Message(
        content= "Hello! I am a chatbot powered by Gemini AI.. How can I help you today?"
    ).send()

# Decorator for handling incoming messages
@cl.on_message
async def handle_message(message: cl.Message):
    """
    Handle the message events from the user
    """
    # Get chat history from user session
    history = cl.user_session.get("history")

    # Add user message to history
    history.append({
        "role": "user",
        "content":message.content
    })

    # Format chat history for Gemini AI
    formatted_history = []
    for msg in history:
        # Determine message role (user or model)
        role = "user" if msg["role"] == "user" else "model"

        # Format message in Gemini-compatible structure
        formatted_history.append(
            {
                "role": role,
                "parts": [
                    {
                        "text": msg["content"]
                    }
                ]
            }
        )
    
    # Generate response using Gemini AI
    response = model.generate_content(formatted_history)

    # Extract response text safely
    response_text = response.text if hasattr(response, 'text') else ""

    # Add assistant's response to history
    history.append(
        {
            "role": "assistant",
            "content":response_text
        }
    )

    # Update session history
    cl.user_session.set("history", history)

    # Send response to user
    await cl.Message(
        content=response_text
    ).send()