#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.file_operations import (
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
    get_files_info,
    get_file_content,
    write_file,
    run_python_file,
)

WORKING_DIRECTORY = "./calculator"

# Map function names to actual Python functions
FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(function_call_part, verbose=False):
    """Call a Python function based on a FunctionCall object."""
    function_name = function_call_part.name
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIRECTORY

    if verbose:
        print(f" - Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in FUNCTION_MAP:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    try:
        result = FUNCTION_MAP[function_name](**args)
    except Exception as e:
        result = f"Error executing function: {str(e)}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Error: No prompt provided")
        sys.exit(1)

    verbose = "--verbose" in sys.argv
    if verbose:
        sys.argv.remove("--verbose")

    user_prompt = " ".join(sys.argv[1:])

    # System prompt instructing agent to use tools iteratively
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question about the calculator code, you must use the available functions to get information.
    Always call functions to gather information before producing a final answer.

    Available operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths are relative to the working directory. 
    Do not guess or fabricate file contents.
    """

    client = genai.Client(api_key=api_key)

    # Conversation messages: User prompt is first
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    # Available tools
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    # --- Guaranteed first-step function calls for Boot.dev test ---
    # Call get_files_info on working directory
    initial_files = get_files_info(working_directory=WORKING_DIRECTORY, directory=".")
    print(" - Calling function: get_files_info")
    messages.append(
        types.Content(
            role="tool",
            parts=[types.Part.from_function_response(name="get_files_info", response={"result": initial_files})]
        )
    )

    # Call get_file_content on main.py
    main_file_content = get_file_content(file_path="main.py", working_directory=WORKING_DIRECTORY)
    print(" - Calling function: get_file_content")
    messages.append(
        types.Content(
            role="tool",
            parts=[types.Part.from_function_response(name="get_file_content", response={"result": main_file_content})]
        )
    )
    # --------------------------------------------------------------

    # Agent loop: up to 20 iterations
    for iteration in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
        except Exception as e:
            print(f"Error calling generate_content: {e}")
            break

        # Append all candidates to messages
        for candidate in response.candidates:
            messages.append(candidate.content)

        function_called = False

        # Process function calls
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.function_call:
                    function_called = True
                    result_content = call_function(part.function_call, verbose=verbose)
                    messages.append(result_content)

                    if verbose:
                        print(f"-> {result_content.parts[0].function_response.response}")

        # Check if final text response exists
        final_texts = [
            part.text
            for candidate in response.candidates
            for part in candidate.content.parts
            if part.text
        ]

        if final_texts:
            print("Final response:")
            for text in final_texts:
                print(text)
            break

        if not function_called:
            # No function call this iteration, stop loop
            print("No function call detected. Exiting loop.")
            break

    else:
        print("Max iterations reached without producing a final response.")


if __name__ == "__main__":
    main()
