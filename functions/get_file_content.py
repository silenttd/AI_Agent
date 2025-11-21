import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file at the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read the file from, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    abs_work = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(full_path)

    if not absolute_path.startswith(abs_work):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(absolute_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        return f"Error: {e}"
    
    return file_content_string