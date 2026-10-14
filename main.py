from src.tools.tool import web_search
from src.pipelines.pipeline import run_research_pipeline

from dotenv import load_dotenv

load_dotenv()  # Forces python to read the .env file manually

# output=web_search("What is the latest news in AGI?")
# print(output)

# r=web_search.invoke("What is the latest news in Artificial General Intelligence?")
# print(r)

topic = " Impact of Artificial Intelligence on society and economy in 2026"
run_research_pipeline(topic)
