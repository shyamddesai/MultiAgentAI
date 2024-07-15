# import json
import json
import os
from crewai import Crew, Process, Agent, Task
from crewai_tools import BaseTool
from langchain_openai import ChatOpenAI

# from MultiAgentAI.crew import (SophisticatedKeywordGeneratorTool, RSSFeedScraperTool, filter_and_categorize_articles,
#                                topic, news_gatherer, news_gathering_task)
from MultiAgentAI.crew.config import relevant_keywords
from MultiAgentAI.crew.crew_tools import market_analysis_tool
from MultiAgentAI.crew.writer import (writer_agent, task)
from MultiAgentAI.crew.sentiment_analysis import (sentiment_analysis_agent, sentiment_analysis_task)
from utils import get_openai_api_key

openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'


# Define the list of commodities
commodity_list = ["Brent", "WTI", "RBOB", "EBOB", "CBOB", "Singapore gasoline R92", "Europe Gasoil",
                  "Marine gasoil 0.5% Singapore", "Far east index propane", "Far east index butane",
                  "Mt Belv Propane", "Mt Belv Butane", "ULSD New york", "asia gasoil", "marine gasoil",
                  "Gold", "Silver"]

# Prompt user to select a commodity
selected_commodity = input(f"Select a commodity from the list: {', '.join(commodity_list)}\n")


class MyCustomTool1(BaseTool):
    name: str = "Saver Tool"
    description: str = "tool used to save output in a json file"

    def _run(self, argument: str) -> str:
        all_articles_output = "./reports/news_output2.json"
        with open(all_articles_output, 'w') as f:
             json.dump(argument, f, indent=2)
        return argument


save_into_json1 = MyCustomTool1()


# Initialize the market analysis agent
market_analysis_agent = Agent(
    role='Market Analyst',
    goal='Analyze market trends for a selected commodity',
    backstory="""You are a seasoned Market Analyst with deep insights into commodity markets.
                 You can quickly identify whether the market is bullish or bearish.""",
    verbose=True,
    allow_delegation=False,
    tools=[market_analysis_tool]
)

# Define the task for the market analysis agent
analysis_task = Task(
    description=selected_commodity,
    expected_output="Market analysis report for the selected commodity saved in a separate json file",
    output_file='market_report.json',
    tool=(save_into_json1),
    agent=market_analysis_agent
)

# Initialize the crew with the task
crew = Crew(
    agents=[writer_agent, market_analysis_agent, sentiment_analysis_agent],
    tasks=[task, analysis_task, sentiment_analysis_task],
    manager_llm=ChatOpenAI(model="gpt-4o", temperature=0.3),
    verbose=2,  # Set verbosity level for logging
    process=Process.sequential  # Use parallel process for asynchronous execution
)

# Kick off the crew to perform the task
result = crew.kickoff()

# Print the result
print("######################")
print(result)

all_articles_output = "./reports/new_output.json"
with open(all_articles_output, 'w') as f:
     json.dump(result, f, indent=2)

# Execute the crew with the input topic

# keywords = SophisticatedKeywordGeneratorTool()._run(topic)
# # save the keywords
# keywords_output = "./reports/keywords_list.json"
# with open(keywords_output, 'w') as f:
#      json.dump(keywords, f, indent=2)

# ------------------------------------------------------------------------------

# keywords_output = "./reports/keywords_list.json"
# with open(keywords_output, 'r') as f:
#      keywords_list = json.load(f)
#
#
#
#
# result = RSSFeedScraperTool()._run(keywords_list)
#
#
#
#
# # Save the articles to JSON, and filter and categorize them
# all_articles_output = "./reports/news_report.json"
# with open(all_articles_output, 'w') as f:
#      json.dump(result, f, indent=2)


# ------------------------------------------------------------------------------

# article_output = "./reports/news_report.json"
#
# filter_and_categorize_articles(article_output)


