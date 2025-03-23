# Import required system modules
import os
# Import for loading environment variables from .env file
from dotenv import load_dotenv
# Import necessary classes from agents module for AI interaction
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# If we use OPENAI model then we onlu need to import Agent and Runner

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# AsyncOpenAI is connecting to OPENAI API connectable APIs asyncronously, we can connecting here with Gemini API using this class
# Initialize AsyncOpenAI provider with Gemini API configuration
provider = AsyncOpenAI(
    api_key = gemini_api_key,
    # Specify the Gemini API endpoint that's compatible with OpenAI format
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

# Create an AI agent instance with specific behavior instructions
agent = Agent(
    # Name of the agent
    name= "Greeting Agent",
    # Detailed instructions for how the agent should respond
    instructions= "You are a Greeting Agent, Your task is to greet the user with a friendly message, when someone says hi you've reply back with Salam from Osama bin Adnan, if someone says bye then say Allah hafiz from Osama bin Adnan, when someone asks other than greeting then say Osama bin Adnan is here just for greeting, I can't answer anything else, Sorry!",
    # Pass the configured model to the agent
    model=model,
)

# Get user input from console
user_question = input("Enter your message: ")

# Run the agent synchronously with user's input
result = Runner.run_sync(
    agent,
    user_question,
)

# Print the agent's response
print(result.final_output)