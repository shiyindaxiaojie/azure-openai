import os

from dotenv import load_dotenv
from langchain.llms import OpenAIChat

load_dotenv()
GPT_API_MODEL = os.getenv("GPT_API_MODEL")
GPT_API_VERSION = os.getenv("GPT_API_VERSION")

chat = OpenAIChat(model_name=GPT_API_MODEL, temperature=0)
chat("Translate this sentence from English to French. I love programming.")
