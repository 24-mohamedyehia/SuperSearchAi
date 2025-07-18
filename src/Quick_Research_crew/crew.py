from crewai import Agent, Crew, Process, Task 
from crewai.project import CrewBase, agent, crew, task 
from Quick_Research_crew.custom_tools import read_search_results_tool, search_multiple_queries_tool
from providers import InintLMM, MakeLLM
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
        self.llm = MakeLLM(self.llm_setting).get_llm()

    @agent
    def QueryGeneratorAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['QueryGeneratorAgent'],
            allow_delegation=False,
            verbose=True,
            memory=True,
            llm=self.llm,
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
            memory=True,
            llm=self.llm,
            tools=[read_search_results_tool]
        )
    
    @task
    def ReportTask(self) -> Task:
        return Task(
            config=self.tasks_config['ReportTask'],
            agent=self.ReportAgent(),
            output_file = os.path.join(os.path.dirname(__file__), f"./research/Research_Report.md")
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