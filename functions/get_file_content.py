import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        abs_work_path = os.path.abspath(working_directory)

        if file_path.startswith(".."):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        abs_file_path = os.path.join(abs_work_path, file_path)

        if not abs_file_path.startswith(abs_work_path):
            return f'Error: Cannot list "{abs_file_path}" as it is outside the permitted working directory'
        

        if not os.path.exists(abs_file_path):
            return f'Error: File not found or is not a regular file: "{abs_file_path}"'
        result = ""
        MAX_CHARS = 10000
        with open(abs_file_path,"r") as f:
            result += f.read(MAX_CHARS)
            if len(f.read()) > MAX_CHARS:
                result+=f'\n [...File "{abs_file_path}" truncated at 10000 characters].'
        return result
    except Exception as E:
        return f"Error: {E}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read a file in the specified path and display the first 10K characters, constrained to the working directory. If the file contains more than 10K characters truncate and show a message",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)