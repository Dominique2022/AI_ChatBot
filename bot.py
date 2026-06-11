import os
from openai import OpenAI #openAI library for python, install with pip install openai


api_key = os.getenv("TOGETHER_API_KEY")
client = OpenAI(api_key=api_key)  #initialize the OpenAI client with the API key

