import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        # Build the full path
        full_path = os.path.join(working_directory, directory)

        # Normalize paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        # Ensure directory is inside the working directory
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if it's a valid directory
        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'

        # Build directory contents string
        lines = []
        for item in os.listdir(abs_full_path):
            try:
                item_path = os.path.join(abs_full_path, item)
                size = os.path.getsize(item_path)
                is_dir = os.path.isdir(item_path)
                lines.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                return f"Error: Could not read info for '{item}' - {str(e)}"

        return "\n".join(lines)

    except Exception as e:
        return f"Error: {str(e)}"


# 👇 Schema for Gemini (so it knows how to call this function)
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. "
                            "If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
