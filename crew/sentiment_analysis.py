import json
import os
from crewai import Agent, Crew, Process, Task
from .crew_tools import SentimentAnalysisTool

sentiment_analysis_output = os.path.join(os.getcwd(), './Data/reports/sources/sources_sentiment.json')

sentiment_analysis_agent = Agent(
    role='Sentiment Analyst',
    goal='Analyze the sentiment of news articles from the provided file',
    backstory="""You are a skilled Sentiment Analyst, adept at gauging the overall sentiment of textual content.
                 You use advanced natural language processing techniques to determine the sentiment score.""",
    verbose=True,
    allow_delegation=False,
    tools=[SentimentAnalysisTool()]
)

sentiment_analysis_task = Task(
    description="Use tool to find and score the Sentiment analysis of each news article",
    expected_output="Sentiment score of each news articles with title and link in json format."
                    "Ensure the output is accurate to the JSON format i.e. use square bracket, double "
                    "quotation marks to define the atrributes, commas to split attributes, does not contain the word "
                    "json, no double quotation marks at the beginning, and no unnecessary backslashes."
                    'Here is an example of the expected JSON output: [{"Title":, "Link":, "Published":, "Relevancy Score":, '
                    '"Relevancy reasoning":, "Sentiment":}]',
    agent=sentiment_analysis_agent,
    output_file=sentiment_analysis_output,
)

crew_sentiment = Crew(
    agents=[sentiment_analysis_agent],
    tasks=[sentiment_analysis_task],
    process=Process.sequential,
    verbose=True
)


# -----------------------------------------------------------------------------

def execute_sentiment_analysis():
    result = crew_sentiment.kickoff()
