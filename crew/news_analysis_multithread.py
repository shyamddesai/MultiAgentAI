import os
import concurrent.futures
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool, BaseTool
import time


file_read_tool = FileReadTool()

directory_path = 'reports/processed_articles/exploration'
all_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

def chunk_list(lst, n):
    return [lst[i::n] for i in range(n)]

num_chunks = 8
num_managers = num_chunks//4
file_chunks = chunk_list(all_files, num_chunks)

agents = []
tasks = []

for i, file_chunk in enumerate(file_chunks):
    agent = Agent(
        role=f'Economic researcher {i}',
        goal=f'Read files in chunk {i}, extract insightful and relevant summaries for the oil and gas market, tailored for ADNOC Global Trading.',
        verbose=True,
        memory=True,
        backstory="You work at ADNOC Global Trading as an economic researcher in the oil and gas energy market. "
        "Your primary objective is to write analytical summaries based on all relevant documents, "
        "focusing on key insights for ADNOC Global Trading.",
        tools=[file_read_tool]
    )
    task = Task(
        description=f"Read and give professional summarizations about the following files: {file_chunk}. "
        "For each file, provide a summary highlighting the key insight relevant to ADNOC global trading or global oil and gas market. ",
        expected_output='Plain texts. For each analyzed document, give its title and summary.',
        tools=[file_read_tool],
        agent=agent
    )
    agents.append(agent)
    tasks.append(task)

crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.sequential,
    memory=True
)
def execute_task(task):
    return task.execute()

def kickoff_parallel(crew):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(execute_task, task) for task in crew.tasks[:-1]]  
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results

parallel_results = kickoff_parallel(crew)
print(len(parallel_results))
print(parallel_results[0])
# result_chunks = chunk_list(parallel_results)

# class Readtool(BaseTool):
#     name : str="Readtool"
#     description : str="Use it to read results of researcher agents!"
#     def _run(self, index)->list:
#         return parallel_results[index]
# readtool=Readtool()


# managers = []
# manager_tasks = []
# for i, results_chunk in enumerate(parallel_results):
#     manager_agent = Agent(
#         role=f'Manager {i}',
#         goal=f'Use the given Readtool, pass parameter {i} to it and get a list of summaries. Then organize them into the same formay and give the final report.',
#         tools=[readtool],
#         verbose=True,
#         memory=True,
#         backstory="You are responsible for reading and merging summaries from resources."
#     )

#     manager_task = Task(
#         description=(
#             "Use given Readtool to read and organize summaries. "
#             " Give a merged final report."
#         ),
#         expected_output='A markdown file containing all summaries. For each entry, contain the title and the summary.'
#         'Do not add other contexts, just give entries of summaries.'
#         ' Each entry has the following format: ## Title: title, newline, ###Summary: newline, summary. ',
#         # output_file='./reports/news_report_analysis_parallel.md',
#         agent=manager_agent
#     )
#     managers.append(manager_agent)
#     manager_tasks.append(manager_task)
# manager_results = ''
# for task in manager_tasks:
#     result = task.execute()
#     manager_results += result+' \n ----------------------------------------'

# with open('./reports/news_report_analysis_parallel.md', 'w') as file:
#     file.write(manager_results)
