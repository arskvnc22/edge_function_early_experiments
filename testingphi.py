from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import json

# --- Assume your Tool class and calculator are in this file ---
from hello import calculator 
available_tools = {
    "calculator": calculator
}

# 1. Download the model FIRST
# repo_id = "mradermacher/Phi-3-mini-4k-instruct-GGUF"
# filename = "Phi-3-mini-4k-instruct.Q4_K_M.gguf"

# print(f"Downloading {filename} from {repo_id}...")
# downloaded_model_path = hf_hub_download(
#     repo_id=repo_id,
#     filename=filename,
#     local_dir=".",
#     local_dir_use_symlinks=False
# )
# print(f"Model downloaded to: {downloaded_model_path}")

# 2. Load the model using the path from the download function
model_path_phi = r"C:\Users\arask\source\repos\edge_function_early_experiments\edge_function_early_experiments\Phi-3-mini-4k-instruct.Q4_K_M.gguf"
llm = Llama(model_path=model_path_phi, n_ctx=2048, verbose=False)
import json
# --- Assuming you have the model loaded and tools.py ready ---
# llm = Llama(...)
# from tools import calculator

# 1. Define the components of the prompt
system_message = "You are a helpful assistant that calls functions by generating a JSON object."
tool_definition = calculator.to_string()

# The few-shot example
example_user_query = "What is 5 + 10?"
example_json_output = '{"tool_name": "calculator", "arguments": {"a": 5, "b": 10}}'

# The final task
final_user_query = "What is the sum of 15 and 28?"

# 3. Create your tool definition and few-shot prompt
# Get the tool definition string dynamically from your imported tool
tool_definition = calculator.to_string() 

user_query = "What is the sum of 15 and 28?"

prompt = f"""<|system|>
{system_message}
You have access to the following tool: {tool_definition}
Your response must be a JSON object.

<|user|>
{example_user_query}

<|assistant|>
{example_json_output}

<|user|>
{final_user_query}

<|assistant|>
"""
print(f"Prompt created:\n{prompt}")

# 4. Get the model's response
output = llm(
    prompt=prompt,
    max_tokens=100,
    stop=["\n", "|"]) # stop at newline or newchat

# 5. Print and parse the result
print("\n" + "-" * 20)
print("Prompt sent to model:")
print(prompt)
print("-" * 20)
print(f"full model output: {output}")
model_output_text = output["choices"][0]["text"]  # Add the closing brace back
print("Model's generated function call:")
print(model_output_text)

try:
    parsed_json = json.loads(model_output_text)
    print("\n✅ JSON is valid.")
    # You can now check parsed_json['tool_name'] and parsed_json['arguments']
    tool_name = parsed_json.get("tool_name")
    arguments = parsed_json.get("arguments")

    # 2. Look up the function in your tool registry
    if tool_name in available_tools:
        function_to_call = available_tools[tool_name]
        
        # 3. Execute the function with the arguments
        print(f"Executing tool: {tool_name} with arguments {arguments}")
        # The ** operator unpacks the dictionary into keyword arguments
        result = function_to_call(**arguments)
        print(f"✅ Tool executed successfully. Result: {result}")

        # 4. Verify the result is correct
        expected_result = 43 # For 15 + 28
        assert result == expected_result
        print(f"✅ Test passed! Result matches expected value.")

    else:
        print(f"❌ Error: Tool '{tool_name}' not found.")

except json.JSONDecodeError as e:
    print(f"\n❌ Invalid JSON: {e}")
except AssertionError:
    print(f"\n❌ Test failed! Result '{result}' does not match expected '{expected_result}'.")
except json.JSONDecodeError as e:
    print(f"\n❌ Invalid JSON: {e}")
