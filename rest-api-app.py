import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_key = os.environ.get("AZURE_OPENAI_KEY")
openai.api_base = os.environ.get("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.environ.get("AZURE_OPENAI_PREVIEW_API_VERSION")

# Example of an OpenAI ChatCompletion request with stream=True
# https://platform.openai.com/docs/guides/chat

# a ChatCompletion request
response = openai.ChatCompletion.create(
    engine='gpt-4-32k',
    messages=[
        {'role': 'user', 'content': "What's 1+1? Answer in one word."}
    ],
    temperature=0,
    stream=True  # this time, we set stream=True
)

for chunk in response:
    print(chunk)