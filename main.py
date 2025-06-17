from src.Research_crew import ResearchCrew
from datetime import datetime
from crewai.flow.flow import Flow, listen, start
import os

class ResearchFlow(Flow):   
    """Flow for Research on any topic"""

    @start()
    def get_user_input(self):
        """Get user input about the topic"""
        print("\n=== Create Your Deep Research ===\n")

        # Get user input
        self.topic = input("What topic would you like to create a research for? :")

    @listen(get_user_input)
    def start_research(self):
        """Create a research on the topic"""
        ResearchCrew().crew().kickoff(inputs={
            'user_query': self.topic,
            'no_keywords': 10,
            'current_date': datetime.now().strftime("%Y-%m-%d"),
            'search_queries': os.path.join('./src/Research_crew/research/step_one_search_queries.json')
        })

def kickoff():
    """Run the guide creator flow"""
    ResearchFlow().kickoff()
    print("\n=== Flow Complete ===")

def plot():
    """Generate a visualization of the flow"""
    flow = ResearchFlow()
    flow.plot("research_flow")

if __name__ == "__main__":
    kickoff()
