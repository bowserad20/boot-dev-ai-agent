import os
from google.genai import types

def run(working_directory, file_path, content):

    try :
        fullPath = os.path.abspath(os.path.join(working_directory, file_path))

        if not fullPath.startswith(os.path.abspath(working_directory)) : 
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        os.makedirs(os.path.dirname(fullPath), exist_ok=True)
        
        with open(fullPath, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e :
        return f"Error: could not write file content due to exception: {e}"

func_declaration = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a new or existing file at the specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file",
            ),
        },
    ),
)