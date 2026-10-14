
import streamlit as st


# Change this import to match your project structure
from src.agents.agent import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Multi-Agent Research Assistant")
st.write(
    "Enter a topic to search the web, gather relevant content, "
    "generate a research report, and receive constructive feedback."
)

# User input
topic = st.text_input(
    "Research topic",
    placeholder="e.g., Generative AI in financial services"
)

run_research = st.button("Generate Research Report", type="primary")

if run_research:
    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    try:
        # Step 1: Search the web
        with st.status("Searching the web...", expanded=True) as status:
            search_agent = build_search_agent()

            search_result = search_agent.invoke({
                "messages": [
                    {"role": "user", "content": f"Search for reliable sources about: {topic}. Return relevant URLs and summaries."}
                ]
            })

            search_messages = search_result["messages"]
            research = search_messages[-1].content

            # Step 2: Read webpage content
            status.update(label="Reading sources...", state="running")

            reader_agent = build_reader_agent()

            reader_result = reader_agent.invoke({
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "Extract the main content from the relevant URLs "
                            "found in this search. Summarize the useful findings "
                            "and retain the source URLs:\n"
                            + research
                        )
                    }
                ]
            })

            reader_messages = reader_result["messages"]
            gathered_research = reader_messages[-1].content

            # Step 3: Generate the report
            status.update(label="Writing research report...", state="running")

            report = writer_chain.invoke({
                "topic": topic,
                "research": gathered_research
            })

            # Step 4: Critique the report
            status.update(label="Reviewing report...", state="running")

            critique = critic_chain.invoke({
                "report": report
            })

            status.update(
                label="Research completed!",
                state="complete",
                expanded=False
            )

        # Display results
        st.subheader("Research Report")
        st.markdown(report)

        st.subheader("Critic's Feedback")
        st.markdown(critique)

        with st.expander("View search results"):
            st.write(research)

        with st.expander("View gathered research"):
            st.write(gathered_research)

    except Exception as e:
        st.error(f"An error occurred: {e}")
