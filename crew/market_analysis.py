import os
from crewai import Agent, Task, Crew, Process
from .crew_tools import market_analysis_tool

def market_analysis(selected_commodity):
    directory_path = f'./Data/marketAnalysis/{selected_commodity}'
    market_analysis_output = os.path.join(os.getcwd(), f'./Data/marketAnalysis/{selected_commodity}/market.json')

    market_analysis_agent = Agent(
        role='Market Analyst',
        goal=f'Analyze market trends for {selected_commodity}',
        backstory="""You are a seasoned Market Analyst with deep insights into commodity markets.
                    You can quickly identify whether the market is bullish or bearish.""",
        verbose=True,
        allow_delegation=False,
        tools=[market_analysis_tool]
    )

    market_analysis_task = Task(
        description=selected_commodity,
        expected_output='A JSON file containing the market analysis for the selected commodity.' 
                        'Take the exact output of the market analysis tool and provide the currrent price, moving average, and trend only.'
                        'Ensure the output is accurate to the JSON format i.e. use square bracket, double quotation marks to define the atrributes, commas to split attributes, does not contain the word json, no double quotation marks at the beginning, and no unnecessary backslashes.'
                        'Here is an example of the expected JSON output: [{"commodity": WTI, "currentPrice": 100, "movingAverage": 90, "trend": ["Bearish"]}]',
        output_file=directory_path+f'/market.json',
        agent=market_analysis_agent,
    )

    # Initialize the Crew
    crew_market = Crew(
        agents=[market_analysis_agent],
        tasks=[market_analysis_task],
        process=Process.sequential,
        verbose=True
    )

    crew_market.kickoff()

    return market_analysis_output

# -----------------------------------------------------------------------------

def execute_market_analysis(selected_commodities):
    try:        
        for selected_commodity in selected_commodities:
            market_analysis_output = market_analysis(selected_commodity)
            print(f"Report saved to {market_analysis_output}")
    except Exception as e:
        print(f"An error occurred: {e}")