import os
from functions.config import MAX_FILE_CONTENT_LENGTH

def get_file_content(working_directory, file_path):
    try:
        # Build full path
        full_path = os.path.join(working_directory, file_path)

        # Normalize paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)

        # Ensure file is inside the working directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure it's a regular file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read file safely
        try:
            with open(abs_file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            return f'Error: Could not read "{file_path}" - {str(e)}'

        # Truncate if too long
        if len(content) > MAX_FILE_CONTENT_LENGTH:
            content = (
                content[:MAX_FILE_CONTENT_LENGTH]
                + f'\n[...File "{file_path}" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'
            )

        return content

    except Exception as e:
        return f"Error: {str(e)}"
