import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):
    try:
        # Build absolute path
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(full_path)

        # Guardrail: file must be inside working_directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if file exists
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'

        # Check if it's a Python file
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Run the Python file
        completed_process = subprocess.run(
            [sys.executable, abs_file_path] + args,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()
        output_lines = []

        if stdout:
            output_lines.append("STDOUT:\n" + stdout)
        if stderr:
            output_lines.append("STDERR:\n" + stderr)
        if completed_process.returncode != 0:
            output_lines.append(f"Process exited with code {completed_process.returncode}")
        if not output_lines:
            return "No output produced."

        return "\n".join(output_lines)

    except Exception as e:
        return f"Error: executing Python file: {str(e)}"
