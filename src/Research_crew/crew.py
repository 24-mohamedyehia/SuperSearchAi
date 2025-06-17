from crewai import Agent, Crew, Process, Task 
from crewai.project import CrewBase, agent, crew, task 
from .providers import ollama , mistral_small
from .models import SuggestedSearchQueries
from .custom_tools import ask_user_tool, search_multiple_queries_tool, read_json_tool
import os

@CrewBase
class ResearchCrew:
    """
    Research Crew for deep search about user query
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def QueryRefinerAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['QueryRefinerAgent'],
            allow_delegation=False,
            verbose=True,
            llm=ollama,
            tools=[ask_user_tool]
        )
    
    @task
    def QueryRefinerTask(self) -> Task:
        return Task(
            config=self.tasks_config['QueryRefinerTask'],
            agent=self.QueryRefinerAgent(),
            output_json=SuggestedSearchQueries,
            output_file = os.path.join(os.path.dirname(__file__), f"research/step_one_search_queries.json")
        )
    
    @agent
    def ResearcherAgent(self) -> Agent:
        return Agent(
            config=self.agents_config['ResearcherAgent'],
            allow_delegation=False,
            verbose=True,
            llm=ollama,
            tools=[read_json_tool, search_multiple_queries_tool]
        ) 
    
    @task
    def ResearcherTask(self) -> Task:
        return Task(
            config=self.tasks_config['ResearcherTask'],
            agent=self.ResearcherAgent()
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