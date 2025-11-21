import os
import subprocess

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