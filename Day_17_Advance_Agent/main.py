# Import required system modules
import os  # For accessing environment variables
import chainlit as cl  # Import Chainlit for chat interface
from dotenv import load_dotenv  # For loading environment variables from .env file
from typing import Dict, Optional  # For type hints
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents import function_tool
# function_tool is a decorator
# By using this function_tool, we can make simple python function into openAI compatible tool
import requests

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# AsyncOpenAI is connecting to OPENAI API connectable APIs asyncronously, we can connecting here with Gemini API using this class
# Initialize AsyncOpenAI provider with Gemini API configuration
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

# OpenAIChatCompletionsModel is a class that is interacting with chat model
# Chat conversional model is of Gemini but compatibilty is of OpenAI
# Configure the chat model using OpenAI-compatible interface
model = OpenAIChatCompletionsModel(
    # Specify the Gemini model version to use
    model="gemini-2.0-flash",
    # Pass the provider configuration
    openai_client=provider,
)

@function_tool("get_asharib_data")
def get_asharib_data() -> str:
    """
    Fetches profile data about Osama bin Adnan from his personal API endpoint.

    This function makes a request to Asharib's profile API and returns information
    about his background, skills, projects, education, work experience, and achievements.

    Returns:
        str: JSON string containing Osama bin Adnan's profile information
    """

    try:
        response = requests.get("https://www.asharib.xyz/api/profile")
        if response.status_code == 200:
            return response.text
        else:
            return f"Error fetching data: Status code {response.status_code}"
    except Exception as e:
        return f"Error fetching data: {str(e)}"


# Create an AI agent instance with specific behavior instructions
agent = Agent(
    name="Greeting Agent",
   instructions="""You are a Greeting Agent designed to provide friendly interactions and information about Osama bin Adnan.

    Your responsibilities:
    1. Greet users warmly when they say hello (respond with 'Salam from Osama bin Adnan')
    2. Say goodbye appropriately when users leave (respond with 'Allah Hafiz from Osama bin Adnan')
    3. When users request information about Osama bin Adnan, use the get_asharib_data tool to retrieve and share his profile information
    4. For any questions not related to greetings or Osama bin Adnan, politely explain: 'I'm only able to provide greetings and information about Osama bin Adnan. I can't answer other questions at this time.'

    Always maintain a friendly, professional tone and ensure responses are helpful within your defined scope.""",

    model=model,
    tools=[get_asharib_data],
)


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
    Handle the message events from the user.
    This function processes each incoming message and manages the conversation flow.
    
    Args:
        message (cl.Message): The incoming message object containing user's input
    """
    # Retrieve the current conversation history from the user's session
    history = cl.user_session.get("history")

    # Add the user's message to conversation history with 'user' role
    history.append({
        "role": "user",
        "content":message.content
    })

    # Run the agent synchronously but wrapped in async execution
    # Runner.run_sync processes the message through the AI agent
    # cl.make_async converts the synchronous operation to asynchronous
    result = await cl.make_async(Runner.run_sync)(agent, input=history)

    # Extract the final response from the agent's result
    response_text = result.final_output

    # Send the agent's response back to the user through the chat interface
    await cl.Message(content= response_text).send()

    # Add the assistant's response to conversation history with 'assistant' role
    # This maintains the complete dialog context for future interactions
    history.append(
        {
            "role": "assistant",
            "content": response_text
        }
    )

    # Update the session with the new conversation history
    # This ensures persistence of the chat context between messages
    cl.user_session.set("history", history)