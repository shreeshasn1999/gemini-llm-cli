import os,subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
        
    abs_work_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    print()
    if not abs_file_path.startswith(abs_work_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        args_list = ["python",abs_file_path]
        if args:
            args_list.extend(args)
        completed_object = subprocess.run(
            args=args_list,
            timeout=30.0,
            capture_output=True,
            text=True,
            cwd=abs_work_path
        )
        output = []
        if completed_object.stdout:
            output.append(f"STDOUT:\n{completed_object.stdout}")
        if completed_object.stderr:
            output.append(f"STDERR:\n{completed_object.stderr}")
        if completed_object.returncode != 0:
            output.append(f"Process exited with code {completed_object.returncode}")
        return "\n".join(output) if output else "No output produced."
    
    except Exception as E:
        return f"Error: executing Python file: {E}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to python file to be run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments to be passed to the function",
            ),
        },
        required=["file_path"]
    ),
)