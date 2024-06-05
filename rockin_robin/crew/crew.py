from crewai import Crew, Task, Agent
from crewai.project import CrewBase, agent, crew, task
from langchain_anthropic import ChatAnthropic
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool, MDXSearchTool
import os


@CrewBase
class ResumeCustomizerCrew:
    """A Crew to customize a resume based on a job posting."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        self.llm = ChatAnthropic(
            model_name="claude-3-sonnet-20240229",
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
            max_tokens=4096,
        )
        self.tool_llm = ChatAnthropic(
            model_name="claude-3-haiku-20240307",
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
        )

        self.scrape_tool = ScrapeWebsiteTool()
        self.search_tool = SerperDevTool()
        self.file_read_tool = FileReadTool(file_path="joshua_oliphant_resume.md")
        self.semantic_search_resume = MDXSearchTool(mdx="joshua_oliphant_resume.md")

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            llm=self.llm,
            function_calling_llm=self.tool_llm,
            tools=[self.search_tool, self.scrape_tool],
            verbose=True,
        )

    @agent
    def profiler(self) -> Agent:
        return Agent(
            config=self.agents_config["profiler"],
            llm=self.llm,
            function_calling_llm=self.tool_llm,
            tools=[
                self.file_read_tool,
                self.semantic_search_resume,
                self.scrape_tool,
                self.search_tool,
            ],
            verbose=True,
        )

    @agent
    def resume_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_strategist"],
            llm=self.llm,
            function_calling_llm=self.tool_llm,
            tools=[
                self.file_read_tool,
                self.semantic_search_resume,
                self.scrape_tool,
                self.search_tool,
            ],
            verbose=True,
        )

    @agent
    def interview_preparer(self) -> Agent:
        return Agent(
            config=self.agents_config["interview_preparer"],
            llm=self.llm,
            function_calling_llm=self.tool_llm,
            tools=[
                self.file_read_tool,
                self.semantic_search_resume,
                self.scrape_tool,
                self.search_tool,
            ],
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.researcher(),
            async_execution=True,
        )

    @task
    def profile_task(self) -> Task:
        return Task(
            config=self.tasks_config["profile_task"],
            agent=self.profiler(),
            async_execution=True,
            output_file="rockin_robin/files/profile.md",
        )

    @task
    def resume_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_strategy_task"],
            agent=self.resume_strategist(),
            context=[self.research_task(), self.profile_task()],
            output_file="rockin_robin/files/tailored_resume.md",
        )

    @task
    def interview_preparation_task(self) -> Task:
        return Task(
            config=self.tasks_config["interview_preparation_task"],
            agent=self.interview_preparer(),
            context=[
                self.research_task(),
                self.profile_task(),
                self.resume_strategy_task(),
            ],
            output_file="rockin_robin/files/interview_materials.md",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, verbose=2)
