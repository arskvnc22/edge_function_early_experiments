from openai import OpenAI
import json

client = OpenAI()
class Agent:
    def __init__(self, client, system_message, name, tools):
        self.name = name
        self.tools = tools
        self.client = client
        self.system_message = system_message
        self.input_list = []
        if self.system_message is not None:
            self.input_list.append({"role": "system", "content": self.system_message})

    def __call__(self, user_query=""):
        self.input_list.append({"role": "user", "content": user_query})
        return self.execute()
    def execute(self):
        response = self.client.responses.create(
            model = "gpt-4o",
            tools = self.tools,
            input = self.input_list,
        )
        print("#########")
        print("#########")
        print(f"response from execute: {response.model_dump_json(indent=2)}")
        print("#########")
        print("#########")
        print(f"response.output: {response.output}")
        print("#########")
        print("#########")
        print("#########")

        return response
system_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

get_planet_mass:
e.g. get_planet_mass: Earth
returns weight of the planet in kg

Example session:

Question: What is the mass of Earth times 2?
Thought: I need to find the mass of Earth
Action: get_planet_mass: Earth
PAUSE 

You will be called again with this:

Observation: 5.972e24

Thought: I need to multiply this by 2
Action: calculate: 5.972e24 * 2
PAUSE

You will be called again with this: 

Observation: 1,1944×10e25

If you have the answer, output it as the Answer.

Answer: The mass of Earth times 2 is 1,1944×10e25.

Now it's your turn:
""".strip()
toolsv1 = [
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
    name="Neil deGrasse Tyson",
    tools=toolsv1
)
def main():
    question = "What is the mass of Earth times 2?"
    response = neil_tyson_agent(question)
    print("Initial response:")
    print(response)


    # for item in response.output:
    #     if item.type == "message":
    #         print(f"🧠 Assistant: {item.content[0].text.strip()}")
    #     elif item.type == "function_call":
    #         function_call = item
    #         function_call_arguments = json.loads(item.arguments)
    #         print(f"Function call detected: {function_call.name} with args {function_call_arguments}")
    #         if function_call.name == "calculator":
    #             result = calculate(function_call_arguments["expression"])
    #             print(f"Result of calculation: {result}")
    #         elif function_call.name == "get_planet_mass":
    #             result = get_planet_mass(function_call_arguments["planet"])
    #             print(f"Mass of {function_call_arguments['planet']}: {result}")
