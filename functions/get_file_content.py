import os
from google.genai import types

MAX_LENGTH = 10000

def run(working_directory, file_path):

    try :
        fullPath = os.path.abspath(os.path.join(working_directory, file_path))

        if not os.path.isfile(fullPath) :
            return f'Error: File not found or is not a regular file: "{file_path}"'

        if not fullPath.startswith(os.path.abspath(working_directory)) : 
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        with open(fullPath, "r") as f:
            output = f.read(MAX_LENGTH)
            if len(output) == MAX_LENGTH :
                output += f'[...File "{file_path}" truncated at 10000 characters]'
            return output
    except Exception as e :
        return f"Error: could not get file content due to exception: {e}"
        
func_declaration = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file at the specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory.",
            ),
        },
    ),
)