import os,sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

def main():
    user_prompt = sys.argv[1]
    isVerbose = len(sys.argv) == 3
    messages = [
        types.Content(role="user",parts=[types.Part(text=user_prompt)])
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages
    )
    print(response.text)
    if isVerbose:
        metadata = response.usage_metadata
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {metadata.prompt_token_count}\nResponse tokens: {metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
