import json
import warnings
from crewai import Crew, Process
from crew import (SophisticatedKeywordGeneratorTool, RSSFeedScraperTool, filter_and_categorize_articles, topic,
                  news_gatherer, news_gathering_task, news_analyst, news_analyst_task)
from MultiAgentAI.crew.config import relevant_keywords
warnings.filterwarnings('ignore')

# ------------------------------------------------------------------------------

crew = Crew(
    agents=[news_gatherer],
    tasks=[news_gathering_task],
    # manager_llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
    process=Process.sequential,
    verbose=False
)

# Execute the crew with the input topic
# keywords = SophisticatedKeywordGeneratorTool()._run(topic)
result = RSSFeedScraperTool()._run(relevant_keywords)

# Save the articles to JSON, and filter and categorize them
all_articles_output = "./reports/news_report.json"
with open(all_articles_output, 'w') as f:
    json.dump(result, f, indent=2)

filter_and_categorize_articles(all_articles_output)

# result = crew.kickoff(inputs={"topic": topic})






