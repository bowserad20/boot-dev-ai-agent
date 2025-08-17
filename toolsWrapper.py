from google.genai import types
import functions
import functions.get_file_content
import functions.get_files_info
import functions.run_python
import functions.write_file

tools: list[types.Tool] = []
funcMap = {}

runnableModules = [functions.get_file_content, functions.get_files_info, functions.run_python, functions.write_file]

tool = types.Tool(function_declarations=[])
for module in runnableModules:
    tool.function_declarations.append(module.func_declaration)
    funcMap[module.func_declaration.name] = module.run
tools.append(tool)

def runFunc(name: str, args: dict[str, any]):
    """
    runs the function by name, and returns that function's return value
    """
    if name in funcMap:
        return funcMap.get(name)(**args)
    raise Exception(f"Unknown function: {name}")

