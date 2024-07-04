from crewai import Agent, Task
from crewai_tools import ScrapeWebsiteTool, FileReadTool
import os
from utils import get_openai_api_key
from dotenv import load_dotenv

load_dotenv()
openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

# ------------------------------------------------------------------------------

scrape_tool = ScrapeWebsiteTool()
file_read_tool = FileReadTool(file_path='./reports/categorized_news_reports/trade_and_export_news_report.json')

news_analyst = Agent(
    role="Oil and Gas Industry Expert News Analyst",
    goal="Extract insightful information based on what is relevant to the oil and gas market that is extracted by the Elite News Aggregator",
    tools=[scrape_tool, file_read_tool],
    backstory="You're working at ADNOC Global Trading as an expert analyst in the oil and gas energy market."
              "You want to write an analytical piece for each of the articles that is relevant to ADNOC. "
            #   "You base your writing on the work of "
            #   "the Elite News Aggregator, who provides the relevant links  "
            #   " about the topic. "
              "You provide accurate strategies and advice with a focus on stock updates like WTI Crude and Brent Crude "
              "and back them up with information like relevant technological breakthroughs and events in the geopolitical environment. "
              "You acknowledge in your piece "
              "when your statements are analysis made by you.",
    verbose=True,
    memory=True,
)

news_analyst_task = Task(
    # description=(
    #     "Your task is to analyze and filter out the articles given to you by the Elite News Aggregator."
    #     "Visit the URLs provided and read the article on the website."
    #     "If the website isn't loading correctly, or requires a subscription to access the page, then ignore the link and move on to the next article."
    #     "Your aim is tailor this for ADNOC Global Trading, who specializes in the trade of refined products."
    #     "Embrace your role and backstory as a expert analyst and make sure the analysis you provide is relevant and insightful to the topics and ADNOC."
    description=(
        "Your task is to analyze and filter out the articles given to you."
        "Visit the URLs provided and read the article on the website."
        "If the website isn't loading correctly, or requires a subscription to access the page, then ignore the link and move on to the next article."
        "Your aim is tailor this for ADNOC Global Trading, who specializes in the trade of refined products."
        # "Group articles together by similarity based on the following categories: incidents and geopoltical news related to the oil and gas market, "
        # "stock-related updates for WTI Crude, Brent Crude, IFAD Murban, ICE Brent, NYMEX WTI, Naphtha, Gasoline, Gasoil 10ppm, Jet Kero, and whatever other stock are relevant to the use case. "
        # "Technological breakthroughs, and currency-related news."
        # "Perform one analysis for each group of articles."
        # "Provide trading strategies if possible based on the "
        # "Embrace your role and backstory as a expert analyst and make sure the analysis you provide is relevant and insightful to the topics and ADNOC."
    ),
    expected_output = "The complete analysis for each of the category groupings."
                    #   "Each grouping to have its own analysis separated."
                      "Provide only the overall analysis for each grouping, but cite the articles as sources",

    # expected_output = "A summary analysis of all the relevant articles/news you deem to be appropraite from the Elite News Aggregator."
    #                   "Each article to have its own analysis seperated.",
    # expected_output="A JSON file containing the list of the collected URLs and their titles from the Elite News Aggregator. "
    #                 "Each entry in the list should be a dictionary with two keys: 'Link' "
    #                 "for the URL and 'Title' for the article's title and 'Summary' for the "
    #                 "expert's analysis. "
    #                 "If an article was skipped over and so has no analysis, explain it in the summary field.",
    output_file='./reports/news_report_analysis.txt',
    agent=news_analyst
)