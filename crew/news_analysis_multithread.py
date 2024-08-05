import os
import concurrent.futures
import json
from dotenv import load_dotenv
from utils import get_openai_api_key
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool

load_dotenv()
openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'

file_read_tool = FileReadTool()
directory_path = f'./reports/processed_articles'
all_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

def chunk_list(lst, n):
    return [lst[i::n] for i in range(n)]

num_chunks = 8
file_chunks = chunk_list(all_files, num_chunks)

agents = []
tasks = []

for i, file_chunk in enumerate(file_chunks):
    agent = Agent(
        role=f'Economic researcher {i}',
        goal=f'Read files in chunk {i}, get title and source from the old title, extract insightful and relevant summaries for the oil and gas market, tailored for ADNOC Global Trading.',
        verbose=True,
        memory=True,
        backstory="You work at ADNOC Global Trading as an economic researcher in the oil and gas energy market. "
        "Your primary objective is to write analytical summaries based on all relevant documents, "
        "focusing on key insights for ADNOC Global Trading.",
        tools=[file_read_tool]
    )

    task = Task(
        description=f"Read and give professional summarizations about the following files: {file_chunk}. "
        "For each file, provide a list of keypoints highlighting the key insight relevant to ADNOC global trading or global oil and gas market. "
        "Keep the origin title and source",
        expected_output='A json file. For each analyzed document, give its title and source and keypoints in the following format: '
        '\{"title":, "source":, "keypoints":[]\}. Use "," to split different summaries and use square bracket to include all summaries. '
        "Don't give answer which is not required, for example, filepath of document, conclusion after summaries, word 'json' or character ''' at beginning. ",
        output_file=directory_path+f'/summary/result{i}.json',
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

# -----------------------------------------------------------------------------

def execute_task(task):
    return task.execute()

def kickoff_parallel(crew):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(execute_task, task) for task in crew.tasks[:-1]]  
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results

# -----------------------------------------------------------------------------

def zuotong():
    parallel_results = kickoff_parallel(crew)
    parallel_results = [json.loads(result) for result in parallel_results]
    parallel_results = [entry for results in parallel_results for entry in results]

    output_path = os.path.join('./Data/reports/reports/report.json')
    with open(output_path, 'w') as file:
        json.dump(parallel_results, file, indent=4)
