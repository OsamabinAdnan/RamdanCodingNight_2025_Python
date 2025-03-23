import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# If we use OPENAI model then we onlu need to import Agent and Runner

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# AsyncOpenAI is connecting to OPENAI API connectable APIs asyncronously, we can connecting here with Gemini API using this class
provider = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)
# OpenAIChatCompletionsModel is a class that is interacting with chat model
# Chat conversional model is of Gemini but compatibilty is of OpenAI
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

agent = Agent(
    name= "Greeting Agent",
    instructions= "You are a Greeting Agent, Your task is to greet the user with a friendly message, when someone says hi you've reply back with Salam from Osama bin Adnan, if someone says bye then say Allah hafiz from Osama bin Adnan, when someone asks other than greeting then say Osama bin Adnan is here just for greeting, I can't answer anything else, Sorry!",
    model=model,
)

user_question = input("Enter your message: ")

result = Runner.run_sync(
    agent,
    user_question,
)

print(result.final_output)