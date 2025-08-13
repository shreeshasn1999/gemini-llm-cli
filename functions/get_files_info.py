import os

def get_files_info(working_directory,directory="."):
    try:
        dir_path = os.path.join(os.path.abspath(working_directory), directory)
        if not dir_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.exists(dir_path):
            return f'Error: "{directory}" is not a directory'
        result = ""
        for file in os.listdir(dir_path):
            result += f"{file}: file_size={os.path.getsize(f"{dir_path}/{file}")} bytes, is_dir={os.path.isdir(f"{dir_path}/{file}")}\n"
        return result
    except Exception as E:
        return f"Error: {E}"