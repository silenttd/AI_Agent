import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments at the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to execute the file from, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    abs_work = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(full_path)

    if not absolute_path.startswith(abs_work):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(absolute_path):
        return f'Error: File "{file_path}" not found.'
    
    if not absolute_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        process_res = subprocess.run(["python", absolute_path] + args, timeout=30, capture_output=True, text=True)
        stdout = process_res.stdout
        stderr = process_res.stderr
        returncode = process_res.returncode
        result = [f"STDOUT: {stdout}", f"STDERR: {stderr}"]

        if returncode != 0:
            result.append(f"Process exited with code {returncode}")
        if not stdout and not stderr:
            result.append(f"No output produced")
    except Exception as e:
        return f"Error: {e}"
    
    return "\n".join(result)