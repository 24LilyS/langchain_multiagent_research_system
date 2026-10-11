from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient # can also import from langchain
from rich import print
from bs4 import BeautifulSoup
# from readibility import Document
import trafilatura 
import re

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

#create a Tavily object using the API key from the environment variable
tavily =TavilyClient(api_key=api_key)

print("Tavily client initialized successfully.")

@tool
def web_search(query:str) -> str:
    """
    Perform a web search using Tavily API and return the results.
    """
    try:
        print ("fetching results from Tavily API...")
        # Use the Tavily client to perform a web search
        response = tavily.search(query, max_results=2)

        out = []
        for r in response["results"]:
            out.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n")
        return "\n.....\n".join(out)
    except Exception as e:
        return f"An error occurred while performing the web search: {str(e)}"

@tool
def scrape_url(url:str) -> str:
    """
    Scrape the content from the url and return text content.
    """
    try:
        print(f"Scraping content from url: {url}")
        # Fetch the content of the URL
        response = requests.get(url,
                                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
                                timeout=15)
        
        response.raise_for_status()  # Raise an error for bad responses

        html_content = response.text

        # Use trafilatura to extract content from the HTML
        print("Attempting to extract content using Trafilatura...")
        text = trafilatura.extract(html_content)


        if not text or len(text.strip()) < 100:
            print("Trafilatura failed to extract useful content, falling back to BeautifulSoup...")
            soup = BeautifulSoup(html_content,'html.parser')

            # Remove script and style elements
            for element in soup(['script','style','nav','footer','header']):
                element.decompose()

            # Get the text
            text = soup.get_text(separator='\n', strip=True)

            # Check if useful content is present
            if not text or len(text.strip()) < 100:
                return "Failed to extract useful content from the URL."
            return "Failed to download content from the URL."

        return text[:10000]  # Return the first 10,000 characters of the content
    except Exception as e:
        return f"An error occurred while scraping the URL: {str(e)}"

if __name__ == "__main__":
    # Example usage
    # query = "What is the latest news in AGI?"
    # results = web_search(query)
    # print(results)

    url= "https://www.theguardian.com/commentisfree/2026/oct/09/ai-climate-change-liability-lawsuits"
    content = scrape_url(url)
    print(content)
