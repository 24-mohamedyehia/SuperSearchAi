from src.Research_crew import ResearchCrew
from src.Report_crew import ReportCrew
from datetime import datetime
from crewai.flow.flow import Flow, listen, start
import os

import agentops
agentops.init()

class ResearchFlow(Flow):   
    """Flow for Research on any topic"""

    @start()
    def get_user_input(self):
        """Get user input about the topic"""
        print("\n=== Create Your Deep Research ===\n")

        # Get user input
        self.topic = input("What topic would you like to create a research for? :")
        self.search_way = input(""" 
                How would you like to search?\n 
                -1) Fast (Snappy responses )\n 
                -2) Deep (High quality Research)\n 
                Enter your choice: """)

    @listen(get_user_input)
    def start_research(self):
        """Create a research on the topic"""
        if self.search_way == "1":
            ResearchCrew().crew().kickoff(inputs={
                'user_query': self.topic,
                'no_keywords': 15,
                'current_date': datetime.now().strftime("%Y-%m-%d"),
                'search_queries': os.path.join('./src/Research_crew/research/step_one_search_queries.json')
            })
        elif self.search_way == "2":
            pass
        
    @listen(start_research)
    def create_report(self):
        """Create a report on the topic"""
        ReportCrew().crew().kickoff(inputs={
            'search_results': os.path.join('./src/Research_crew/research/all_search_results.json'),
            'user_query': self.topic
        })

def kickoff():
    """Run the guide creator flow"""
    ResearchFlow().kickoff()
    print("\n=== Flow Complete ===")

if __name__ == "__main__":
    kickoff()
