from crewai import Agent, Crew, Process, Task 
from crewai.project import CrewBase, agent, crew, task 
from providers import get_deepseek_v3, InintLMM
from custom_tools import read_json_tool
import os

@CrewBase
class ReportCrew:   
    """
    Report Crew for deep search about user query
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, llm_setting: InintLMM):
        self.llm_setting = llm_setting

    @agent
    def ReportAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['ReportAgent'],
            allow_delegation=False,
            verbose=True,
            llm=get_deepseek_v3(self.llm_setting),
            tools=[read_json_tool]
        )
    
    @task
    def ReportTask(self) -> Task:
        return Task(
            config=self.tasks_config['ReportTask'],
            agent=self.ReportAgent(),
            output_file = os.path.join(os.path.dirname(__file__), f"./final_report/Deep_Research_Report.html")
        )
    
    @crew
    def crew(self) -> Crew:
        """
        Creates the research crew
        """
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.sequential,
            verbose=True
        )