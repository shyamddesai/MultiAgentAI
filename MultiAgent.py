import json
import os
import sys
from crewai import Crew, Process, Agent, Task
from crewai_tools import BaseTool
from langchain_openai import ChatOpenAI

# Determine the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Check if the .venv folder is in the current directory
if os.path.exists(os.path.join(current_dir, '.venv')):
    project_root = current_dir
else:
    project_root = os.path.dirname(current_dir)

# Add the parent directory of MultiAgentAI to the PYTHONPATH
sys.path.append(os.path.dirname(project_root))

# Print to check the PYTHONPATH
# print(f"Project root: {project_root}")
# print(f"PYTHONPATH: {sys.path}")

from MultiAgentAI.crew.news_filter_tools import filter_and_categorize_articles
from MultiAgentAI.crew.config import topic, relevant_keywords, commodity_list
from MultiAgentAI.crew.crew_tools import market_analysis_tool, SophisticatedKeywordGeneratorTool, RSSFeedScraperTool
from MultiAgentAI.crew.writer import (writer_agent, writer_task)
from MultiAgentAI.crew.sentiment_analysis import (sentiment_analysis_agent, sentiment_analysis_task)
from MultiAgentAI.crew.news_ranker import news_ranker, news_rank_task, output_file_path_rank
from MultiAgentAI.crew.preprocess_articles import process_all_json_files, process_articles
from utils import get_openai_api_key

openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

# Read the selected keywords from the file in user_data directory
keywords_file = os.path.join(os.getcwd(), 'Frontend', 'user_data', 'selected_keywords.txt')
if os.path.exists(keywords_file):
    with open(keywords_file, 'r') as f:
        selected_keywords = f.read().splitlines()
else:
    selected_keywords = ["no keywords found"]  # Default value if the file doesn't exist
print(f"Selected keywords: {selected_keywords}")


# Read the selected words from the file
commodities_file = os.path.join(os.getcwd(), 'Frontend', 'user_data', 'selected_commodities.txt')
if os.path.exists(commodities_file):
    with open(commodities_file, 'r') as f:
        selected_commodities = f.read().splitlines()
else:
    selected_commodities = ["no commodities found"]  # Default value if the file doesn't exist
print(f"Selected words: {selected_commodities}")

# keywords = SophisticatedKeywordGeneratorTool()._run(topic)
# # save the keywords
# keywords_output = "./reports/keywords_list.json"
# with open(keywords_output, 'w') as f:
#      json.dump(keywords, f, indent=2)
#      print("keywords saved in json file")
#
# # ------------------------------------------------------------------------------
#
# keywords_output = "./reports/keywords_list.json"
# with open(keywords_output, 'r') as f:
#      keywords_list = json.load(f)

# result = RSSFeedScraperTool()._run(keywords_list)


# # Save the articles to JSON, and filter and categorize them
# all_articles_output = "./reports/news_report.json"
# with open(all_articles_output, 'w') as f:
#      json.dump(result, f, indent=2)
# ------------------------------------------------------------------------------

article_output = "./reports/news_report.json"
# filtered_articles = filter_and_categorize_articles(article_output)
# process_articles(filtered_articles) # Scrape the articles and cleanse the HTML content

process_articles("./reports/filtered_news_report.json")


# preprocessing and zuotong sth sth

# ranking -----------------------------------------------------------------------


# Initialize the Crew
crew_rank = Crew(
    agents=[news_ranker],
    tasks=[news_rank_task],
    process=Process.sequential,
    verbose=True
)

# # Execute the rank Crew
# try:
#     result = crew_rank.kickoff()
#     with open(output_file_path_rank, 'w') as f:
#         json.dump(result, f, indent=2)
#     print(f"Results saved to {output_file_path_rank}")
# except Exception as e:
#     print(f"An error occurred: {e}")

# sentiment ---------------------------------------------------------------------

output_file_path_sentiment = os.path.join(os.getcwd(), './reports/sentiment_analysis.json')

# Initialize the Crew
crew_sentiment = Crew(
    agents=[sentiment_analysis_agent],
    tasks=[sentiment_analysis_task],
    process=Process.sequential,
    verbose=True
)

# # Execute the sentiment Crew
# try:
#     result = crew_sentiment.kickoff()
#     with open(output_file_path_sentiment, 'w') as f:
#         json.dump(result, f, indent=2)
#     print(f"Results saved to {output_file_path_sentiment}")
# except Exception as e:
#     print(f"An error occurred: {e}")

# Market Analysis #########################################

output_file_path_market = os.path.join(os.getcwd(), './reports/market_analysis.json')

# Prompt user to select a commodity
selected_commodity = input(f"Select a commodity from the list: {', '.join(commodity_list)}\n")


market_analysis_agent = Agent(
    role='Market Analyst',
    goal='Analyze market trends for a selected commodity',
    backstory="""You are a seasoned Market Analyst with deep insights into commodity markets.
                 You can quickly identify whether the market is bullish or bearish.""",
    verbose=True,
    allow_delegation=False,
    tools=[market_analysis_tool]
)

market_analysis_task = Task(
    description=selected_commodity,
    expected_output="Market analysis report for the selected commodity",
    agent=market_analysis_agent,

)

# Initialize the Crew
crew_market = Crew(
    agents=[market_analysis_agent],
    tasks=[market_analysis_task],
    process=Process.sequential,
    verbose=True
)

# Kick off the market crew to perform the task
# try:
#     result = crew_market.kickoff()
#     print(f"Report saved to {output_file_path_market}")
# except Exception as e:
#     print(f"An error occurred: {e}")
#
# # Additional error handling for saving results
# try:
#     with open(output_file_path_market, 'w') as f:
#         json.dump(result, f, indent=2)
#     print(f"Results saved to {output_file_path_market}")
# except Exception as e:
#     print(f"An error occurred while saving the results: {e}")

#Writer Agent ###############################################

input_file_path_report = os.path.join(os.getcwd(), '../reports/news_report_analysis_parallel.md')
output_file_path_report = os.path.join(os.getcwd(), '../reports/final_news_report.json')


# Initialize the crew with the task
crew = Crew(
    agents=[writer_agent],
    tasks=[writer_task],
    manager_llm=ChatOpenAI(model="gpt-4o", temperature=0.3),
    verbose=2,  # Set verbosity level for logging
    process=Process.sequential  # Use sequential process for execution
)

# Kick off the writing crew to perform the task
# try:
#     result = crew.kickoff()
#     print(f"Report saved to {output_file_path_report}")
# except Exception as e:
#     print(f"An error occurred: {e}")
#
# # Additional error handling for saving results
# try:
#     with open(output_file_path_report, 'w') as f:
#         json.dump(result, f, indent=2)
#     print(f"Results saved to {output_file_path_report}")
# except Exception as e:
#     print(f"An error occurred while saving the results: {e}")
