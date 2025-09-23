from google.genai import types
import os
import subprocess

# --- Function Implementations ---

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'

        lines = []
        for item in os.listdir(abs_full_path):
            item_path = os.path.join(abs_full_path, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            lines.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(lines)

    except Exception as e:
        return f"Error: {str(e)}"


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_full_path):
            return f'Error: "{file_path}" is not a file'

        with open(abs_full_path, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        return f"Error: {str(e)}"


def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        with open(abs_full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Successfully wrote to {file_path}"

    except Exception as e:
        return f"Error: {str(e)}"


def run_python_file(working_directory, file_path, args=None):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot run "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_full_path):
            return f'Error: "{file_path}" is not a file'

        cmd = ["python", abs_full_path]
        if args:
            cmd += args

        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout + result.stderr

    except Exception as e:
        return f"Error: {str(e)}"


# --- Function Declarations (Schemas) ---

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory to list files from, relative to the working directory.",
            )
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file relative to the working directory."
            )
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(type=types.Type.STRING),
            "content": types.Schema(type=types.Type.STRING),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(type=types.Type.STRING),
            "args": types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
        },
    ),
)
