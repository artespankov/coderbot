import os
from google.genai import types

def get_files_info(working_directory, directory=None):

    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    else:
        target_dir = os.path.abspath(working_directory)

    if not target_dir.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        content = []
        for name in os.listdir(target_dir):
            filepath = os.path.join(target_dir, name)
            content.append(f'- {name}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}')
        return '\n'.join(content)
    except Exception as e:
        return f"Error: {e}"
    

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