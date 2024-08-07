import os
import sys
from utils import get_openai_api_key

# Determine the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Check if the project directory name is as expected for the imports to work correctly
if 'MultiAgentAI' in current_dir:
    project_root = current_dir
else:
    project_root = os.path.dirname(current_dir)

# Add the project root directory to the PYTHONPATH
sys.path.append(project_root)

from crew.config import user_input_commodities, user_input_keywords
from crew.news_analysis_multithread import zuotong
from crew.postprocess_articles import process_json_file
from crew.preprocess_articles import split_articles
from crew.summary_writer import execute_summary_writer
from crew.sentiment_analysis import execute_sentiment_analysis
from crew.news_ranker import execute_news_ranker
from crew.cherry_picking import cherry_picking
from crew.market_analysis import execute_market_analysis

openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

# -----------------------------------------------------------------------------

def process_before_agents():
    cherry_picking(user_input_keywords())

    process_json_file('./reports/FINAL_Filter_by_keywords.json', './reports/FINAL_Filter_by_keywords.json')
    print("Files cleaned!")

    split_articles('./reports/FINAL_Filter_by_keywords.json')

    execute_market_analysis(user_input_commodities())


######################################### Cherry Picking #########################################

process_before_agents()

######################################### Zuotong #########################################

zuotong()

######################################### Ranking Agent #########################################

execute_news_ranker()

######################################### Sentiment Analysis #########################################

execute_sentiment_analysis()


######################################### Highlights Writer #########################################

execute_summary_writer()


# -----------------------------------------------------------------------------

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
