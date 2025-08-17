import os
from google.genai import types

def run(working_directory, directory="."):
    try :
        fullPath = os.path.abspath(os.path.join(working_directory, directory))

        if not os.path.isdir(fullPath) :
            return f'Error: "{directory}" is not a directory'

        if not fullPath.startswith(os.path.abspath(working_directory)) : 
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        output = ""
        for name in os.listdir(fullPath):
            filePath = os.path.join(fullPath, name)
            output += f"""
            - {name}: file_size={os.path.getsize(filePath)} bytes, is_dir={os.path.isdir(filePath)}
            """
        return output
    except Exception as e:
        return f"Error: could not get file info due to exception: {e}"

func_declaration = types.FunctionDeclaration(
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