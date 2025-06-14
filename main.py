import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# SYSTEM_PROMPT = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
SYSTEM_PROMPT = """
You are a helpful AI coding agent.
When a user asks a question or makes a request, make a function call plan. 
You can perform the following operations:
- List files and directories
All paths you provide should be relative to the working directory. 
You do not need to specify the working directory in your function calls 
as it is automatically injected for security reasons.
"""

AVAILABLE_FUNCTIONS = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)




def main():

    while len(sys.argv) < 2:
        print("Provide your prompt as a program argument")
        sys.exit(1)

    user_prompt = sys.argv[1]
    verb = False
    if len(sys.argv) > 2 and sys.argv[2]=='--verbose':
        verb = True
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]


    gemini = genai.Client(api_key=api_key)
    generated_response = gemini.models.generate_content(
        model='gemini-2.0-flash-001',  # free tier model
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[AVAILABLE_FUNCTIONS])
    )
    # if generated_response.function_calls:
    for function_call_part in generated_response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(generated_response.text)
    if verb:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {generated_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {generated_response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()