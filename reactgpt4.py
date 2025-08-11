from openai import OpenAI
import json
from dotenv import load_dotenv
import os
import re

load_dotenv()  

api_key_open = os.getenv("OPENAI_API_KEY")
client = OpenAI(
     api_key = api_key_open,
    #  project = "Default project",
)
if api_key_open:
    # Print the first 7 and last 4 characters to verify without exposing the full key
    print("API Key Loaded Successfully.")
    print(f"   Using key starting with: {api_key_open[:7]}... and ending with: ...{api_key_open[-4:]}")
else:
    print("ERROR: OpenAI API Key not found. Check your .env file and variable name.")

class Agent:
    def __init__(self, client, system_message, name):
        self.name = name
        #self.tools = tools
        self.client = client
        self.system_message = system_message
        self.input_list = []
        if self.system_message is not None:
            self.input_list.append({"role": "system", "content": self.system_message})

    def __call__(self, user_query=""):
        if user_query:
             self.input_list.append({"role": "user", "content": user_query})
        result = self.execute()
        print("*************************")
        print("result:")
        print("result:")
        print("*************************")
        print (result)
        print("*************************")
        print("result:")
        print("result:")
        print("*************************")
        #self.input_list.append({"role": "user", "content": user_query})
        assistant_message = result.choices[0].message.content
        print(f"assistant_message: {assistant_message}")
        self.input_list.append({"role": "assistant", "content": assistant_message})

        return result
    def execute(self):
        response = self.client.chat.completions.create(
            model = "gpt-4o",
            #tools = self.tools,
            messages = self.input_list,
        )
        print("Response from execute:")
        print(response.model_dump_json(indent=2))
        print("*************************")
        print("*************************")
        print (self.input_list)
        print("*************************")
        print("*************************")

        return response
system_prompt = """
You run in a loop of Thought, PAUSE, Action, PAUSE, Observation.
At the end of the loop you output an Answer
When it is your turn you will only output a thought, action or observation. Do not output them all at once.
After you output a Thought, you will be called again with Observation: OK.
Use Thought to describe your thoughts about the question you have been asked. Thats the only output you will make until you output an Action. You will be prompted again with Observation: OK.
Use PAUSE to indicate youre turn is over.
Use Action to run one of the actions available to you. Then output what the next step should be - then return PAUSE.
You will be called again with the output of the action you ran, which is called Observation.
Observation will be the result of running those actions.
**IMPORTANT** :

DO NOT output everything at once, only output Thought, you will be prompted again.
Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

get_planet_mass:
e.g. get_planet_mass: Earth
returns weight of the planet in kg

Example session:

User:
Question: What is the mass of Earth times 2?

Assistant:
Thought: I need to find the mass of Earth
PAUSE

You will be called again with this:
User:
Observation: OK
Assistant:
Action: get_planet_mass: Earth
PAUSE 


You will be called again with this:
User:
Observation: 5.972e24

Assistant:
Thought: I need to multiply this by 2
PAUSE


You will be called again with this:
User:
Observation: OK

Assistant:
Action: calculate: 5.972e24 * 2
PAUSE


You will be called again with this:             

User:
Observation: 1,1944×10e25

Assistant:
Thought: I have the mass of Earth times 2, which is 1,1944×10e25. I will output this as the final answer.
PAUSE

User:
Observation: OK
Assistant:
Action: <FINISH>: The mass of Earth times 2 is 1,1944×10e25.
PAUSE



Now we start. Do not output everything at once, only output Thought, then PAUSE, then Action, .
""".strip()
toolsv1 = [ # ok here is the problem im having with regards to the structure of the steps: the model cant effectively know what the next step should be after the action unless it has received the observation. One solution might be to output the next step after the observation using the same adapter. That would add quite a bit of complexity
    {
        "type": "function",
        "name": "calculator",
        "description": "Performs simple arithmetic.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A math expression like '2 + 2 * 3'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "type": "function",
        "name": "get_planet_mass",
        "description": "Returns the mass of a planet in kg.",
        "parameters": {
            "type": "object",
            "properties": {
                "planet": {
                    "type": "string",
                    "description": "Name of the planet, e.g. Earth, Mars"
                }
            },
            "required": ["planet"]
        }
    }
]
def calculate(operation):
    return eval(operation) # demo purpose

def get_planet_mass(planet):
    planet_masses = {
        "earth": 5.972e24,
        "mars": 6.4171e23,
        "jupiter": 1.8982e27,
        "saturn": 5.6834e26,
        "venus": 4.8675e24,
        "mercury": 3.3011e23
    }
    planet = planet.lower()
    return planet_masses.get(planet, None)

neil_tyson_agent = Agent(
    client=client,
    system_message=system_prompt,
    name="Neil deGrasse Tyson"
    #tools=toolsv1
)
def while_loop(initial_prompt):
    print("Starting Neil deGrasse Tyson agent...")
    finish = False
    iternum = 0
    maxiternum = 7
    tools = ["calculate", "get_planet_mass"]
    next_prompt = initial_prompt
 
    
    while finish == False or iternum < maxiternum:
     
        response = neil_tyson_agent(next_prompt)


        iternum += 1
        print(f"\nIteration {iternum} of {maxiternum}")
        
        message = response.choices[0].message
        role = message.role  # "assistant" or "user"
        content = message.content
        if role == "assistant":
            
            if content.startswith("Thought:"):
                next_prompt = "Observation: OK"
            elif content.startswith("Action:"):
                action = re.findall(r"Action: ([a-z_]+): (.+)", content, re.IGNORECASE)
                print(f"Action to perform: {action}")
                chosen_tool = action[0][0]
                arg = action[0][1]
                print(f"Chosen tool: {chosen_tool}, Argument: {arg}")
                if chosen_tool in tools:
                    if chosen_tool == "calculate":
                        action_result = calculate(arg)
                        next_prompt = f"Observation: {action_result}"
                    elif chosen_tool == "get_planet_mass":
                        action_result = get_planet_mass(arg)
                        next_prompt = f"Observation: {action_result}"

            
            if "<FINISH>" in content:
                print("Final Answer:", content.text.replace("Answer:", "").strip())
                finish = True

    print("\nConversation History:")
    for message in neil_tyson_agent.input_list:
        print(f"{message['role'].capitalize()}: {message['content']}")
def main():
    while_loop("Question: What is the mass of Mars times 5?")
    
        

if __name__ == "__main__":
        main()


