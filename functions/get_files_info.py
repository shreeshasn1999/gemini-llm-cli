import os
from google.genai import types
def get_files_info(working_directory,directory="."):
    abs_work_path = os.path.abspath(working_directory)
    abs_dir_path = os.path.abspath(os.path.join(working_directory, directory))
    try:

        if not abs_dir_path.startswith(abs_work_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        

        if not os.path.exists(abs_dir_path):
            return f'Error: "{directory}" is not a directory'
        result = ""
        for file in os.listdir(abs_dir_path):
            result += f"{file}: file_size={os.path.getsize(f"{abs_dir_path}/{file}")} bytes, is_dir={os.path.isdir(f"{abs_dir_path}/{file}")}\n"
        return result
    except Exception as E:
        return f"Error: {E}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)