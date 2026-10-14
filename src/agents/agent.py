from langchain.agents import create_agent
from langchain_openai   import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tool import web_search, scrape_url
from dotenv import load_dotenv
import os

load_dotenv()  # Forces python to read the .env file manually

# Model initialization
llm  = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, max_tokens=1000)

# First Agent: Search Agent
def build_search_agent():
    """
    Build and return a search agent that can perform web searches.
    """
    tools = [web_search]
    
    # Create a chat prompt template for the agent
    # prompt_template = ChatPromptTemplate.from_messages([
    #     ("system", "You are a helpful assistant that can perform web searches on the following query."),
    #     ("user", "{input}")

    # ])
    
    # Create the agent with the specified tools and prompt template
    agent = create_agent(
        model=llm,
        tools=tools,
        # prompt=prompt_template,
          )
    
    return agent

# Second Agent: Reader Agent
def build_reader_agent():
    """
    Build and return a reader agent that can scrape content from URLs.
    """
    tools = [scrape_url]
    
    # Create a chat prompt template for the agent
    # prompt_template = ChatPromptTemplate.from_messages([
    #     ("system", "You are a helpful assistant that can scrape content from the provided URL."),
    #     ("user", "{input}")
    # ])
    
    # Create the agent with the specified tools and prompt template
    agent = create_agent(
        model=llm,
        tools=tools,
        # prompt=prompt_template,
    )
    
    return agent

# writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research writer. write clear , structured and insightful research report."),
    ("human", """write a detailed research report on a topic below

     Topic: {topic}

     Research_gathered: {research}

     Sructure the report as :
     - Introduction
     - key Findings (minimum 3 well explained points)
     - Conclusion
     - References (list all url foound in the research)

     Be detailed, factual, and professional."""),
])

writer_chain =  writer_prompt | llm | StrOutputParser()


# Crtic Chain

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp constructive research critic. Be honest and specific."),
    ("human", """Critique the research report below and provide constructive feedback.

     Research Report: {report}

     Provide your critique in a structured format:
     - Score (1-10): Rate the overall quality of the report.
     - Strengths: Highlight the strong points of the report.
     - Weaknesses: Point out areas that need improvement or are lacking.
     - Suggestions: Offer specific suggestions for enhancing the report.

     Be detailed, factual, and professional."""),
])

critic_chain =  critic_prompt | llm | StrOutputParser()
