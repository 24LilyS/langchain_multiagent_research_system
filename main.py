from src.tools.tool import web_search
import os

from dotenv import load_dotenv

load_dotenv()  # Forces python to read the .env file manually

# output=web_search("What is the latest news in AGI?")
# print(output)

r=web_search.invoke("What is the latest news in Artificial General Intelligence?")
print(r)