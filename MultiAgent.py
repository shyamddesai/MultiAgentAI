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

from MultiAgentAI.crew import (SophisticatedKeywordGeneratorTool, RSSFeedScraperTool, filter_and_categorize_articles,
                               topic, news_gatherer, news_gathering_task)
from MultiAgentAI.crew.config import relevant_keywords, commodity_list
from MultiAgentAI.crew.crew_tools import market_analysis_tool
from MultiAgentAI.crew.news_analysis_multithread import zuotong
from MultiAgentAI.crew.postprocess_articles import process_json_file
from MultiAgentAI.crew.preprocess_articles import split_articles
from MultiAgentAI.crew.writer import (writer_agent, writer_task)
from MultiAgentAI.crew.sentiment_analysis import (sentiment_analysis_agent, sentiment_analysis_task)
from utils import get_openai_api_key
from MultiAgentAI.crew.news_ranker import news_ranker, news_rank_task, output_file_path_rank
from MultiAgentAI.crew.cherry_picking import filter_articles_by_keywords_in_title_or_content, CherryPicking

openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'


def userInputKeywords():
    # # Read the selected keywords from the file in user_data directory
    keywords_file = os.path.join(os.getcwd(), 'Frontend', 'data', 'userInput', 'selected_keywords.txt')
    if os.path.exists(keywords_file):
        with open(keywords_file, 'r') as f:
            selected_keywords = f.read().splitlines()
            print(f"Selected keywords: {selected_keywords}")
            return selected_keywords
    else:
        selected_keywords = ["no keywords found"]  # Default value if the file doesn't exist
        return 1


def userInputCommodities():
    # Read the selected words from the file
    commodities_file = os.path.join(os.getcwd(), 'Frontend', 'data', 'userInput', 'selected_commodities.txt')
    if os.path.exists(commodities_file):
        with open(commodities_file, 'r') as f:
            selected_commodities = f.read().splitlines()
            print(f"Selected words: {selected_commodities}")
            return selected_commodities
    else:
        selected_commodities = ["no commodities found"]  # Default value if the file doesn't exist
        return 1


selected_keywords = userInputKeywords()
selected_commodities = userInputCommodities()





# CherryPicking(selected_keywords)

# process_json_file('./reports/FINAL_Filter_by_keywords.json', './reports/FINAL_Filter_by_keywords.json')


# split_articles('./reports/FINAL_Filter_by_keywords.json')



# preprocessing and zuotong sth sth

# zuotong function
# zuotong()
# ranking -----------------------------------------------------------------------

# Initialize the Crew

crew_rank = Crew(
    agents=[news_ranker],
    tasks=[news_rank_task],
    process=Process.sequential,
    verbose=True
)

# Execute the rank Crew
# try:
# result = crew_rank.kickoff()
#     with open(output_file_path_rank, 'w') as f:
#         json.dump(result, f, indent=2)
#     print(f"Results saved to {output_file_path_rank}")
# except Exception as e:
#     print(f"An error occurred: {e}")

##IMPORTANT fix format code here

# sentiment ---------------------------------------------------------------------



# Initialize the Crew
crew_sentiment = Crew(
    agents=[sentiment_analysis_agent],
    tasks=[sentiment_analysis_task],
    process=Process.sequential,
    verbose=True
)

# # Execute the sentiment Crew
# try:
# result = crew_sentiment.kickoff()
#     with open(output_file_path_sentiment, 'w') as f:
#         json.dump(result, f, indent=2)
#     print(f"Results saved to {output_file_path_sentiment}")
# except Exception as e:
#     print(f"An error occurred: {e}")

##IMPORTANT fix format code here


# Market Analysis #########################################


# Prompt user to select a commodity
# selected_commodity = input(f"Select a commodity from the list: {', '.join(commodity_list)}\n")

def marketAnalysis(selected_commodity):
    # output_file_path_market = os.path.join(os.getcwd(), f'./Data/marketAnalysis/{selected_commodity}/market.json')

    directory_path = f'./Data/marketAnalysis/{selected_commodity}'

    market_analysis_agent = Agent(
        role='Market Analyst',
        goal=f'Analyze market trends for {selected_commodity}',
        backstory="""You are a seasoned Market Analyst with deep insights into commodity markets.
                    You can quickly identify whether the market is bullish or bearish.""",
        verbose=True,
        allow_delegation=False,
        tools=[market_analysis_tool]
    )

    market_analysis_task = Task(
        description=selected_commodity,
        expected_output='A JSON file containing the market analysis for the selected commodity.' 
                        'Take the exact output of the market analysis tool and provide the currrent price, moving average, and trend only.'
                        'Ensure the output is accurate to the JSON format i.e. use square bracket, double quotation marks to define the atrributes, commas to split attributes, does not contain the word json, no double quotation marks at the beginning, and no unnecessary backslashes.'
                        'Here is an example of the expected JSON output: [{"commodity": WTI, "currentPrice": 100, "movingAverage": 90, "trend": ["Bearish"]}]',
        output_file=directory_path+f'/market.json',
        agent=market_analysis_agent,
    )

    # Initialize the Crew
    crew_market = Crew(
        agents=[market_analysis_agent],
        tasks=[market_analysis_task],
        process=Process.sequential,
        verbose=True
    )

    crew_market.kickoff()

# Kick off the market crew to perform the task
# try:

# for selected_commodity in selected_commodities:
#     marketAnalysis(selected_commodity)

    # print(f"Report saved to {output_file_path_market}")
# except Exception as e:
# print(f"An error occurred: {e}")

# Additional error handling for saving results
# try:
#     with open(output_file_path_market, 'w') as f:
#         json.dump(result, f, indent=2)
#     print(f"Results saved to {output_file_path_market}")
# except Exception as e:
#     print(f"An error occurred while saving the results: {e}")

# Writer Agent ###############################################


# Initialize the crew with the task
highlight_crew = Crew(
    agents=[writer_agent],
    tasks=[writer_task],
    manager_llm=ChatOpenAI(model="gpt-4o", temperature=0.1),
    verbose=2,  # Set verbosity level for logging
    process=Process.sequential  # Use sequential process for execution
)

# Kick off the writing crew to perform the task
result = highlight_crew.kickoff()

print("done")


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
#
# result = RSSFeedScraperTool()._run(keywords_list)
#
#
# # Save the articles to JSON, and filter and categorize them
# all_articles_output = "./reports/news_report.json"
# with open(all_articles_output, 'w') as f:
#      json.dump(result, f, indent=2)
# # ------------------------------------------------------------------------------
#
# article_output = "./reports/news_report.json"
#
# filter_and_categorize_articles(article_output)
