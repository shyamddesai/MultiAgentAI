import os
import concurrent.futures
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool, BaseTool
import time


file_read_tool = FileReadTool()

directory_path = 'reports/categorized_news_reports/cleaned_exploration'
all_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

def chunk_list(lst, n):
    return [lst[i::n] for i in range(n)]

num_chunks = 4 
file_chunks = chunk_list(all_files, num_chunks)

agents = []
tasks = []

for i, file_chunk in enumerate(file_chunks):
    agent = Agent(
        role=f'Reader {i}',
        goal=f'Read files in chunk {i}, extract insightful and relevant summaries for the oil and gas market, tailored for ADNOC Global Trading.',
        verbose=True,
        memory=True,
        backstory="You work at ADNOC Global Trading as an expert analyst in the oil and gas energy market. "
        "Your primary objective is to write analytical summaries based on all relevant documents, "
        "focusing on key insights for ADNOC Global Trading.",
        tools=[file_read_tool]
    )
    task = Task(
        description=f"Read and summarize the following files: {file_chunk}. " 
        "Focus on the 'CleanedContent' part of each file. "
        "For each file, provide a one-line summary of the 'CleanedContent', highlighting the key insights relevant to ADNOC global trading.",
        expected_output='A text file containing one-line summaries for each analyzed document.',
        tools=[file_read_tool],
        agent=agent
    )
    agents.append(agent)
    tasks.append(task)
parallel_results=[]

class Readtool(BaseTool):
    name : str="Readtool"
    description : str="Use it to read results of reader agents!"
    def _run(self)->list:
        return parallel_results
    
readtool=Readtool()
manager_agent = Agent(
    role='Manager',
    goal='Coordinate reading and summarizing tasks and merge the final report.',
    tools=[readtool],
    verbose=True,
    memory=True,
    backstory="You are responsible for managing the task and merging summaries from other agents."
)

manager_task = Task(
    description=(
        "Coordinate the reading and summarizing tasks of other reader agents."
        " Collect their results and merge a final report."
    ),
    expected_output='A compiled summary report of all files.',
    output_file='./reports/news_report_analysis_parallel.md',
    agent=manager_agent
)

agents.append(manager_agent)
tasks.append(manager_task)

def execute_task(task):
    return task.execute()

def kickoff_parallel(crew):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(execute_task, task) for task in crew.tasks[:-1]]  
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results

crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.sequential,
    memory=True
)


start = time.time()
parallel_results = kickoff_parallel(crew)
final_result = manager_task.execute()
end = time.time()
print(final_result)
print(end-start)
