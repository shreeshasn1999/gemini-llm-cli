import os

def get_file_content(working_directory, file_path):
    try:
        file_path = os.path.join(working_directory, file_path)

        if working_directory not in file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        result = ""
        for file in os.listdir(file_path):
            result += f"{file}: file_size={os.path.getsize(f"{file_path}/{file}")} bytes, is_dir={os.path.isdir(f"{file_path}/{file}")}\n"
        return result
    except Exception as E:
        return f"Error: {E}"