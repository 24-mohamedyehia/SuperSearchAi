from crewai import Agent, Crew, Process, Task 
from crewai.project import CrewBase, agent, crew, task 
from providers import InintLMM, MakeLLM
from .custom_tools import serper_search_tool, extract_links_and_save, scrape_tool, get_knowledge_json_paths
from .custom_tools import file_json_read_tool
from crewai_tools import FileReadTool
import os

file_read_tool = FileReadTool()

@CrewBase
class DeepResearchCrew():
    """
    Deep Research Crew for deep search about user query
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, llm_setting: InintLMM):
        self.llm_setting = llm_setting
        self.llm = MakeLLM(self.llm_setting).get_llm()

    @agent
    def PlanningAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['PlanningAgent'],
            allow_delegation=False,
            verbose=True,
            memory=True,
            llm=self.llm,
        )
    
    @task
    def PlanningTask(self) -> Task:
        return Task(
            config=self.tasks_config['PlanningTask'],
            agent=self.PlanningAgent(),
            output_file = os.path.join(os.path.dirname(__file__), f"./research_results/Research_Planning.md")
        )
    
    @agent
    def WebSearchAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['WebSearchAgent'],
            allow_delegation=False,
            verbose=True,
            memory=True,
            llm=self.llm,
            tools=[serper_search_tool, extract_links_and_save]
        )

    @task
    def WebSearchTask(self) -> Task:
        return Task(
            config=self.tasks_config['WebSearchTask'],
            agent=self.WebSearchAgent()
        )
    
    @agent
    def WebScraperAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['WebScraperAgent'],
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
            tools=[scrape_tool]
        )

    @task
    def WebScraperTask(self) -> Task:
        return Task(
            config=self.tasks_config['WebScraperTask'],
            agent=self.WebScraperAgent()
        )

    @agent
    def ReportWriterAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['ReportWriterAgent'],
            allow_delegation=False,
            verbose=True,
            memory=True,
            llm=self.llm,
            tools=[get_knowledge_json_paths,
                file_json_read_tool]
        )

    @task
    def ReportWriterTask(self) -> Task:
        return Task(
            config=self.tasks_config['ReportWriterTask'],
            agent=self.ReportWriterAgent(),
            output_file = os.path.join(os.path.dirname(__file__), f"./research_results/Research_Report.md")
        )

    @crew
    def crew(self) -> Crew:
        """
        Creates the deep research crew
        """
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.sequential,
            verbose=True
        )
