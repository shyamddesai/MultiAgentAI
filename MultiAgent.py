import json
import warnings
from crewai import Crew, Process
from crew import (SophisticatedKeywordGeneratorTool, RSSFeedScraperTool, filter_and_categorize_articles, topic,
                  news_gatherer, news_gathering_task, news_analyst, news_analyst_task)

warnings.filterwarnings('ignore')

crew = Crew(
    # agents=[news_gatherer, news_analyst],
    # tasks=[news_gathering_task, news_analyst_task],
    agents=[news_analyst],
    tasks=[news_analyst_task],
    #manager_llm=ChatOpenAI(model="gpt-3.5-turbo",temperature=0.7),
    process=Process.sequential,
    verbose=False
)

# # Execute the crew with the input topic
# keywords = SophisticatedKeywordGeneratorTool()._run(topic)
# result = RSSFeedScraperTool()._run(keywords)

# # Save the articles to JSON, and filter and categorize them
# all_articles_output = "./reports/news_report.json"
# with open(all_articles_output, 'w') as f:
#     json.dump(result, f, indent=2)

# filter_and_categorize_articles(all_articles_output)

result = crew.kickoff(inputs={"topic": topic})






