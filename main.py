#!/usr/bin/env python3
"""
AI-Agent main script
Generates a response from the Gemini 2.0 model using a Content object.
Supports a --verbose flag for detailed output.
"""

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types  # Import types for Content and Part


def main():
    # Check if at least one argument (the prompt) is provided
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command line argument.")
        print("Usage: uv run main.py \"Your prompt here\" [--verbose]")
        sys.exit(1)

    # Detect --verbose flag
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.remove("--verbose")  # remove it from the args list

    # Combine all remaining arguments into one string as the user prompt
    user_prompt = " ".join(sys.argv[1:])

    # Load API key from .env
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found! Check your .env file.")

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    # Create a list of Content objects
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    # Generate content using messages
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    # Print response
    print("Response:")
    print(response.text)

    # If verbose, print additional info
    if verbose:
        print("\nVerbose info:")
        print(f'User prompt: "{user_prompt}"')
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
