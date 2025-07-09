from crewai import Agent, Crew, Process, Task 
from crewai.project import CrewBase, agent, crew, task 
from providers import get_mistral_small, get_deepseek_v3
from .models import QuickReport
from Quick_Research_crew.custom_tools import read_json_tool, search_multiple_queries_tool
from providers import InintLMM
import os

@CrewBase
class ResearchCrew():
    """
    Research Crew for quick search about user query
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, llm_setting: InintLMM):
        self.llm_setting = llm_setting
        self.mistral_small = get_mistral_small(self.llm_setting)
        self.deepseek_v3 = get_deepseek_v3(self.llm_setting)

    @agent
    def QueryGeneratorAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['QueryGeneratorAgent'],
            allow_delegation=False,
            verbose=True,
            llm=self.mistral_small,
            tools=[search_multiple_queries_tool]
        )
    
    @task
    def QueryGenerationTask(self) -> Task:
        return Task(
            config=self.tasks_config['QueryGenerationTask'],
            agent=self.QueryGeneratorAgent()
        )

    @agent
    def ReportAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['ReportAgent'],
            allow_delegation=False,
            verbose=True,
            llm=self.deepseek_v3,
            tools=[read_json_tool]
        )
    
    @task
    def ReportTask(self) -> Task:
        return Task(
            config=self.tasks_config['ReportTask'],
            agent=self.ReportAgent(),
            output_json= QuickReport,
            output_file = os.path.join(os.path.dirname(__file__), f"./research/Research_Report.json")
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