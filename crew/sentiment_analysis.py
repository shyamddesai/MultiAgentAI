from crewai_tools import BaseTool
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from crewai import Agent, Task


#
# class SentimentAnalysisTool(BaseTool):
#     name: str = "Sentiment Analysis Tool"
#     description: str = "Reads news articles from a file and performs sentiment analysis."
#
#     def __init__(self, file_path: str):
#         self.file_path = file_path
#
#     def _run(self):
#         # Read the file
#         with open(self.file_path, 'r') as file:
#             news_articles = file.read()
#
#         # Perform sentiment analysis
#         sentiment_score = self.perform_sentiment_analysis(news_articles)
#         return sentiment_score
#
#     def perform_sentiment_analysis(self, news_articles: str) -> float:
#         analyzer = SentimentIntensityAnalyzer()
#         sentences = news_articles.split('\n')
#         sentiment_score = sum(analyzer.polarity_scores(sentence)["compound"] for sentence in sentences) / len(sentences)
#         return sentiment_score
#
#     def __call__(self):
#         return self._run()
#
#
# sentiment_analysis_tool = SentimentAnalysisTool(file_path='C:/Users/Laith/PycharmProjects/ProjectMultiAgent/MultiAgentAI/reports/news_report_analysis_parallel.md')
#
#
# sentiment_analysis_agent = Agent(
#     role='Sentiment Analyst',
#     goal='Analyze the sentiment of news articles from the provided file',
#     backstory="""You are a skilled Sentiment Analyst, adept at gauging the overall sentiment of textual content.
#                  You use advanced natural language processing techniques to determine the sentiment score.""",
#     verbose=True,
#     allow_delegation=True,
#     tools=[sentiment_analysis_tool]
# )
#
#
# # Define the sentiment analysis task
# sentiment_analysis_task = Task(
#     description="Sentiment analysis of each news article",
#     expected_output="Sentiment score of the provided news articles",
#     agent=sentiment_analysis_agent
# )
