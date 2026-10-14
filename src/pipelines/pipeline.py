from src.agents.agent import build_search_agent, build_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic:str) -> dict:
    state = {} 

    print("\n"+"="*50)
    print("Search Agent is working ..........")
    print("="*50)

    # Step 1: Use the Search Agent to gather information

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, relaible and detailed information about the topic '{topic}'")]
    })

    state['search_agent'] = search_result['messages'][-1].content
    print("\n search results", state['search_agent']) 

    #Step 2 : Use the Reader Agent to scrape content from the most relevant URL
    print("\n"+"="*50)
    print("Reader Agent is working ..........")
    print("="*50)
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
                      f"Based on the following search result about  '{topic}',"
                      f"Pick the most relevant URL and scrape it for deeper content.\n\n"
                      f"Search results:\n{state['search_agent'][:800]}")]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\n scraped content", state['scraped_content'])


    # Step 3: Use the Writer Chain to generate a research report

    print("\n"+"="*50)
    print("Writer is drafting a report ..........")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS: {state['search_agent']}\n\n"
        f"DETAILED_SCRAPED_CONTENT: {state['scraped_content']}"

)

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n"+"="*50)
    print("Research Report Generated Successfully!")
    print("="*50)
    print(f"Generated Final Report: {state['report']}")


    # Step 4: Use the Critic Chain to evaluate the report

    print("\n"+"="*50)
    print("Critic is evaluating the report ..........")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        'topic': topic,
        'report': state["report"]
    })

    print("\n"+"="*50)
    print("Critic Feedback Received Successfully!")
    print("="*50)
    print(f"Critic Feedback: {state['feedback']}")

    return state
