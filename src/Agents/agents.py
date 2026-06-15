from langchain.agents import create_agent
#from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.Tools.tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# Model Initialization
#llm = ChatOpenAI(model = "gpt-4o-mini",temperature=0)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# 1st Agent : Search Agent
def build_search_agent():
    return create_agent(
        model= llm,
        tools=[web_search],
        system_prompt="""
You are a search agent.
Your job is ONLY to call the web_search tool and return its results.

Rules:
- Return raw search results only.
- Include Title, URL, and Snippet exactly.
- Prefer credible sources.
- Avoid Quora, Reddit, forums, and low-quality blogs.
- Do not summarize.
"""
       
    )

# 2nd Agent : Reader Agent
def build_reader_agent():
    return create_agent(
        model= llm,
        tools=[scrape_url],
        system_prompt="""
You are a research reader agent.

Rules:
- Do not scrape only one URL unless only one URL is available.
- Scrape at least 3 URLs from the search results.
- Prefer credible sources: universities, scientific journals, government sites, established news/research organizations.
- Avoid Quora, forums, Reddit, and commercial blogs unless no better sources exist.
- If a URL returns 403, timeout, or scraping error, skip it and scrape the next URL.
- Return the scraped content grouped by URL.
- Preserve each source URL in the final answer.
"""

    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()




#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()