import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_work_path = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_file_path.startswith(abs_work_path):
            return f'Error: Cannot list "{abs_file_path}" as it is outside the permitted working directory'
        
        with open(abs_file_path,"w+") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as E:
        return f"Error: {E}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or Overwrites to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write/overwrite to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write/overwrite in the file,with the given path",
            ),
        },
    ),
)