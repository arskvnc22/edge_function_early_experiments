from openai import OpenAI
import json

client = OpenAI()

# Initial state
question = "What is (4 + 6) * 3?"
input_list = [{"role": "user", "content": question}]
tools_used = []
tools = [
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
    }
]
def calculator(expression: str):
    try:
        return str(eval(expression))  # Unsafe in prod — safe here for demo
    except Exception as e:
        return f"Error: {str(e)}"
class Agent:
    def __init__(self, client, system_message, name, tools):
        self.name = name
        self.tools = tools

for step in range(5):
    print(f"\n🔁 Step {step + 1}")

    # Send to GPT
    response = client.responses.create(
        model="gpt-4o",
        tools=tools,
        input=input_list,
        instructions="You are an agent and you work in a ReAct style loop (Thought-action-observation). When you receive a question start by thinking step by step about the question, thinking about what tools to use. Before using a tool, think step-by-step and explain your reasoning. ",
    )

    for item in response.output:
        print(f"🧾 Item Type: {item.type}")

        if item.type == "message":
            # Check if this is the final answer
            msg = item.content[0].text.strip()
            print(f"🧠 Assistant: {msg}")
            input_list.append({"role": "assistant", "content": msg})
            if "Answer:" in msg:
                print("✅ Final Answer Reached.")
                exit()
        
        elif item.type == "function_call":
            print(f" Tool Call: {item.name} with args {item.arguments}")
            args = json.loads(item.arguments)
            call_id = item.call_id

            # Run the function locally
            if item.name == "calculator":
                result = calculator(args["expression"])
                print(f"📥 Observation: {result}")

                # Add the tool call + result to input list
                input_list.append(item)  # function_call item
                input_list.append({
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": json.dumps({"result": result}),
                })
