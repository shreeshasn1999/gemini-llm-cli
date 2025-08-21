import os,sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info,get_files_info
from functions.get_file_content import schema_get_file_content,get_file_content
from functions.write_file import schema_write_file,write_file
from functions.run_python_file import schema_run_python_file,run_python_file

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def call_function(function_call_part, verbose=False):
    function_dict = {
        "get_file_content":get_file_content,
        "get_files_info":get_files_info,
        "write_file":write_file,
        "run_python_file":run_python_file
    }
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")
    
    if function_dict[function_call_part.name] is None:
        return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )
    
    function_result = function_dict[function_call_part.name](working_directory="./calculator",**function_call_part.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

def main():
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    user_prompt = sys.argv[1]
    isVerbose = len(sys.argv) == 3
    messages = [
        types.Content(role="user",parts=[types.Part(text=user_prompt)])
    ]
    available_functions = [
        types.Tool(function_declarations=[schema_get_files_info]),
        types.Tool(function_declarations=[schema_get_file_content]),
        types.Tool(function_declarations=[schema_run_python_file]),
        types.Tool(function_declarations=[schema_write_file]),
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=available_functions,
            system_instruction=system_prompt
        )
    )
    print(response.text)
    function_call_list = response.function_calls
    for call in function_call_list:
        function_call_result = call_function(call,isVerbose)
        print(f"-> {function_call_result.parts[0].function_response.response}")
    if isVerbose:
        metadata = response.usage_metadata
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {metadata.prompt_token_count}\nResponse tokens: {metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
