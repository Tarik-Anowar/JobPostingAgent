import threading
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.agents import initialize_agent
from langchain.tools import Tool
from langchain.agents import AgentType

system_message = """You are an AI job post generator that interacts with humans step by step to collect job details. 
You ask one question at a time, validate responses, and ensure completeness.  
Once all details are collected, ask for confirmation before finalizing.  

After the user confirms "Yes," store all details and return "Done."

Job Post Schema:
- Job Title
- Company Name
- Job Location

Rules:
1. Collect data step by step.
2. Validate responses dynamically.
3. If a response is incorrect, re-ask the question.
4. After collecting all responses,you must display the data you collected in markdown format them to the user and ask if they are satisfied.
5. If the user wants to update any field, allow them to make changes.
6. Once the user is satisfied, ask:
   "Would you like to submit this job post? (Yes/No)"
7. If the user confirms "Yes," store all responses synchronously and return "Done."
"""

class JobPostCollector:
    def __init__(self):
        self.job_details = {}

    def add_response(self, key, value):
        """Stores user responses dynamically."""
        print(f"{key}: {value} added")
        self.job_details[key] = value

    def get_job_details(self):
        """Returns all collected job details."""
        return self.job_details

    def missing_fields(self, required_fields):
        """Identifies and returns any missing fields."""
        return [field for field in required_fields if field not in self.job_details]

    def clear_data(self):
        """Clears stored responses to start fresh."""
        self.job_details = {}


import ast  

def add_response_tool(inputs):
    """Stores job details dynamically in the JobPostCollector."""
    
    print(f"Received input: {inputs}")
    print(f"Type of input: {type(inputs)}")

    if isinstance(inputs, str):
        try:
            inputs = ast.literal_eval(inputs)  
        except (SyntaxError, ValueError):
            return "Error: Invalid input format. Could not parse string to dictionary."

    if not isinstance(inputs, dict):
        return "Error: Invalid input format. Expected a dictionary."

    for key, value in inputs.items():
        if key and value:
            client.collector.add_response(key, value)

    return "Done"


add_response = Tool(
    name="add_response",
    func=add_response_tool,
    description="Use this tool to store job details dynamically."
)


class GeminiClient:
    def __init__(self, api_key, user_id):
        self.api_key = api_key
        self.user_id = user_id
        self.collector = JobPostCollector()
        self.model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=self.api_key)
        self.history = [SystemMessage(content=system_message)]
        self.agent = initialize_agent(
            tools=[add_response],
            llm=self.model,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def run_agent_in_background(self):
        """Runs the agent in a separate thread (non-blocking)."""
        thread = threading.Thread(target=self.agent.run, args=(self.history,))
        thread.start()

    def generate_content(self, prompt):
        """Generates AI response using Gemini 1.5 Flash"""
        self.history.append(HumanMessage(content=prompt))

        if "Would you like to submit this job post?" in self.history[-2].content and prompt.lower() == "yes":
            self.run_agent_in_background()
            return "Done"

        response = self.model.invoke(self.history)

        ai_response = response if isinstance(response, str) else response.content
        self.history.append(AIMessage(content=ai_response))
        
        return ai_response


API_KEY = "AIzaSyDSmCWzo2dJ-4ksvUzjsz2y5OnaI9BBeds"
client = GeminiClient(API_KEY, user_id="12345")


def interact_with_agent(query):
    """Handles the conversation with the AI agent."""
    res = client.generate_content(query)
    print(client.collector.get_job_details())  # Print job details for debugging
    return res
