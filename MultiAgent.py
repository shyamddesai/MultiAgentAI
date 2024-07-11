import json
from crewai import Crew, Process
from MultiAgentAI.crew import (SophisticatedKeywordGeneratorTool, RSSFeedScraperTool, filter_and_categorize_articles,
                               topic, news_gatherer, news_gathering_task, news_analyst, news_analyst_task)
from MultiAgentAI.crew.config import relevant_keywords


# ------------------------------------------------------------------------------

# crew = Crew(
#     agents=[news_gatherer],
#     tasks=[news_gathering_task],
#     # manager_llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
#     process=Process.sequential,
#     verbose=False
# )

# Execute the crew with the input topic

# keywords = SophisticatedKeywordGeneratorTool()._run(topic)
# # save the keywords
# keywords_output = "./reports/keywords_list.json"
# with open(keywords_output, 'w') as f:
#      json.dump(keywords, f, indent=2)

# ------------------------------------------------------------------------------

keywords_output = "./reports/keywords_list.json"
with open(keywords_output, 'r') as f:
     keywords_list = json.load(f)




result = RSSFeedScraperTool()._run(keywords_list)




# Save the articles to JSON, and filter and categorize them
all_articles_output = "./reports/news_report.json"
with open(all_articles_output, 'w') as f:
     json.dump(result, f, indent=2)


# ------------------------------------------------------------------------------

# article_output = "./reports/news_report.json"
#
# filter_and_categorize_articles(article_output)

# result = crew.kickoff(inputs={"topic": topic})