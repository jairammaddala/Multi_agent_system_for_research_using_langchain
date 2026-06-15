import streamlit as st
from src.Agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 AI Research Assistant")
st.caption("Search, read, draft, and critique research reports using your agent pipeline.")

def run_research_pipeline(topic: str) -> dict:
    state = {}

    progress = st.progress(0)
    status = st.empty()

    with st.expander("Step 1: Search Results", expanded=True):
        status.info("Search agent is working...")
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [(
                "user",
                f"Search this topic and return raw results with URLs: {topic}"
            )]
        })
        state["search_results"] = search_result["messages"][-1].content
        st.write(state["search_results"])
        progress.progress(25)

    with st.expander("Step 2: Scraped Content", expanded=True):
        status.info("Reader agent is scraping top resources...")
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [(
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state["scraped_content"] = reader_result["messages"][-1].content
        st.write(state["scraped_content"])
        progress.progress(50)

    with st.expander("Step 3: Final Report", expanded=True):
        status.info("Writer is drafting the report...")
        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )

        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
        })

        st.markdown(state["report"])
        progress.progress(75)

    with st.expander("Step 4: Critic Feedback", expanded=True):
        status.info("Critic is reviewing the report...")
        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })

        st.markdown(state["feedback"])
        progress.progress(100)

    status.success("Research pipeline completed.")
    return state


with st.sidebar:
    st.header("Research Settings")
    topic = st.text_input(
        "Research topic",
        placeholder="Example: AI agents in healthcare",
    )

    run_button = st.button("Run Research", type="primary", use_container_width=True)

    st.divider()
    st.caption("Built with Streamlit + LangChain agents")


if run_button:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("Running research pipeline..."):
            result = run_research_pipeline(topic)

        st.subheader("Download Results")

        full_output = f"""
# Research Topic
{topic}

# Search Results
{result["search_results"]}

# Scraped Content
{result["scraped_content"]}

# Final Report
{result["report"]}

# Critic Feedback
{result["feedback"]}
"""

        st.download_button(
            label="Download Full Research Report",
            data=full_output,
            file_name=f"{topic.replace(' ', '_')}_research_report.md",
            mime="text/markdown",
        )
else:
    st.info("Enter a topic in the sidebar and click **Run Research**.")