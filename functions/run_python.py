import subprocess
import os
from google.genai import types

def run(working_directory, file_path, args=[]):
    try:
        fullPath = os.path.abspath(os.path.join(working_directory, file_path))

        if not os.path.isfile(fullPath) :
            return f'Error: File "{file_path}" not found'
        
        if not fullPath.endswith('.py') :
            return f'Error: "{file_path}" is not a Python file'

        if not fullPath.startswith(os.path.abspath(working_directory)) : 
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        res = subprocess.run(["python3", str(fullPath), *args], cwd=working_directory, capture_output=True, timeout=30)
        
        if (not res.stdout) and (not res.stderr) and (res.returncode != 0):
            return "No output produced"
        
        return f"""
        STDOUT: {res.stdout}
        STDERR: {res.stderr}
        {"" if res.returncode == 0 else "Process exited with code " + res.returncode}
        """
    except Exception as e:
        return f"Error: executing Python file: {e}"

func_declaration = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the python file at the specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments to pass via the CLI when running the python file, as an array of strings",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="each argument to be added, as a string"
                )
            ),
        },
    ),
)