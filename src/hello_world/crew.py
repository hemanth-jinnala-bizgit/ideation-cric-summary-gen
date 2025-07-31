import os
import sys
from dotenv import load_dotenv

# SQLite fix for ChromaDB on Streamlit Cloud
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew

from src.hello_world.tools.cricket_api_tools import (
    ScorecardTool,
    MatchInfoTool,
    HighlightsTool,
    CommentaryTool,
    MatchSummaryTool
)

@CrewBase
class HelloWorld():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml' 

    def __init__(self):
        self.llm = LLM(model=os.getenv("MODEL"))
        self.cricket_tools = [
            MatchSummaryTool(), ScorecardTool(), MatchInfoTool(),
            HighlightsTool(), CommentaryTool()
        ]

    # === OPTIMIZED AGENTS (Only 4 super-powered agents) ===
    @agent
    def summary_writer(self) -> Agent:
        return Agent(config=self.agents_config['summary_writer'], llm=self.llm, verbose=True, tools=self.cricket_tools)

    @agent
    def mega_analyst(self) -> Agent:
        return Agent(config=self.agents_config['mega_analyst'], llm=self.llm, verbose=True, tools=self.cricket_tools)

    @agent
    def viral_master(self) -> Agent:
        return Agent(config=self.agents_config['viral_master'], llm=self.llm, verbose=True, tools=self.cricket_tools)

    @agent
    def ultimate_digest_master(self) -> Agent:
        return Agent(config=self.agents_config['ultimate_digest_master'], llm=self.llm, verbose=True)

    # === OPTIMIZED TASKS (Only 4 tasks for maximum speed) ===
    @task
    def get_final_match_result(self) -> Task:
        return Task(config=self.tasks_config['get_final_match_result'], agent=self.summary_writer())

    @task
    def generate_main_summary(self) -> Task:
        return Task(config=self.tasks_config['generate_main_summary'], agent=self.summary_writer(), context=[self.get_final_match_result()])

    @task
    def extract_mega_highlights(self) -> Task:
        return Task(config=self.tasks_config['extract_mega_highlights'], agent=self.mega_analyst(), context=[self.generate_main_summary()])


    @task
    def generate_ultimate_match_digest(self) -> Task:
        return Task(
            config=self.tasks_config['generate_ultimate_match_digest'], 
            agent=self.ultimate_digest_master(), 
            context=[
                self.get_final_match_result(),
                self.generate_main_summary(), 
                self.extract_mega_highlights()
            ]
        )

    # === CREW ===
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )