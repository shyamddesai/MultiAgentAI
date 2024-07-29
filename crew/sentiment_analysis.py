import os
from crewai import Agent, Task
from pydantic import BaseModel
from crewai_tools import BaseTool
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from MultiAgentAI.crew.crew_tools import market_analysis_tool
from MultiAgentAI.crew.config import relevant_keywords, commodity_list


output_file_path_sentiment = os.path.join(os.getcwd(), './Data/reports/sources/sources_sentiment.json')

class SentimentAnalysisTool(BaseTool, BaseModel):
    name: str = "Sentiment Analysis Tool"
    description: str = "Reads news articles from a file and performs sentiment analysis."
    file_path: str = os.path.join(os.getcwd(), './Data/reports/sources/sources_ranked.json')

    def _run(self):
        # Read the file
        with open(self.file_path, 'r') as file:
            news_articles = file.read()

        # Split the file content into individual articles
        articles = news_articles.split('\n\n')  # Assuming each article is separated by two newlines

        # Perform sentiment analysis on each article
        results = []
        for article in articles:
            sentiment_score = self.perform_sentiment_analysis(article)
            sentiment = "positive" if sentiment_score > 0 else "negative"
            results.append({
                "article": article,
                "sentiment": sentiment
            })

        return results

    def perform_sentiment_analysis(self, article: str) -> float:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_score = analyzer.polarity_scores(article)["compound"]
        return sentiment_score

    def __call__(self):
        return self._run()


sentiment_analysis_tool = SentimentAnalysisTool()

sentiment_analysis_agent = Agent(
    role='Sentiment Analyst',
    goal='Analyze the sentiment of news articles from the provided file',
    backstory="""You are a skilled Sentiment Analyst, adept at gauging the overall sentiment of textual content.
                 You use advanced natural language processing techniques to determine the sentiment score.""",
    verbose=True,
    allow_delegation=False,
    tools=[sentiment_analysis_tool]
)

# Define the sentiment analysis task
sentiment_analysis_task = Task(
    description="Use tool to find and score the Sentiment analysis of each news article",
    expected_output="Sentiment score of each news articles with title and link in json format."
                    "Ensure the output is accurate to the JSON format i.e. use square bracket, double "
                    "quotation marks to define the atrributes, commas to split attributes, does not contain the word "
                    "json, no double quotation marks at the beginning, and no unnecessary backslashes."
                    'Here is an example of the expected JSON output: [{"Title":, "Link":, "Published":, "Relevancy Score":, '
                    '"Relevancy reasoning":, "Sentiment":}]',
    agent=sentiment_analysis_agent,
    output_file=output_file_path_sentiment,
)

