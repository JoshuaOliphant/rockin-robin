from crewai import Crew, Task, Agent, Process
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileReadTool, MDXSearchTool
import os
from dotenv import load_dotenv

load_dotenv()


@CrewBase
class ResumeCustomizerCrew:
    """A Crew to customize a resume based on a job posting."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, resume_file_path) -> None:
        self.tool_llm = ChatOpenAI(
            model_name=os.environ.get("TOOL_MODEL_NAME"),
            api_key=os.environ.get("TOOL_MODEL_API_KEY"),
            max_tokens=os.environ.get("TOOL_MODEL_MAX_TOKENS"),
            base_url=os.environ.get("TOOL_MODEL_BASE_URL"),
        )
        self.aggregator_llm = ChatOpenAI(
            model_name=os.environ.get("AGGREGATOR_MODEL_NAME"),
            api_key=os.environ.get("AGGREGATOR_MODEL_API_KEY"),
            max_tokens=os.environ.get("AGGREGATOR_MODEL_MAX_TOKENS"),
            base_url=os.environ.get("AGGREGATOR_MODEL_BASE_URL"),
        )
        self.proposer1 = ChatOpenAI(
            model_name=os.environ.get("PROPOSER_MODEL_NAME1"),
            api_key=os.environ.get("PROPOSER_MODEL_API_KEY1"),
            max_tokens=os.environ.get("PROPOSER_MODEL_MAX_TOKENS1"),
            base_url=os.environ.get("PROPOSER_MODEL_BASE_URL1"),
        )
        self.proposer2 = ChatOpenAI(
            model_name=os.environ.get("PROPOSER_MODEL_NAME2"),
            api_key=os.environ.get("PROPOSER_MODEL_API_KEY2"),
            max_tokens=os.environ.get("PROPOSER_MODEL_MAX_TOKENS2"),
            base_url=os.environ.get("PROPOSER_MODEL_BASE_URL2"),
        )
        self.proposer3 = ChatOpenAI(
            model_name=os.environ.get("PROPOSER_MODEL_NAME3"),
            api_key=os.environ.get("PROPOSER_MODEL_API_KEY3"),
            max_tokens=os.environ.get("PROPOSER_MODEL_MAX_TOKENS3"),
            base_url=os.environ.get("PROPOSER_MODEL_BASE_URL3"),
        )

        self.scrape_tool = ScrapeWebsiteTool()
        self.search_tool = SerperDevTool()
        self.file_read_tool = FileReadTool(file_path=resume_file_path)
        self.semantic_search_resume = MDXSearchTool(mdx=resume_file_path)

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            llm=self.aggregator_llm,
            function_calling_llm=self.tool_llm,
            tools=[self.search_tool, self.scrape_tool],
            verbose=True,
            cache=True,
        )

    @agent
    def profiler(self) -> Agent:
        return Agent(
            config=self.agents_config["profiler"],
            llm=self.aggregator_llm,
            function_calling_llm=self.tool_llm,
            tools=[
                self.file_read_tool,
                self.semantic_search_resume,
                self.scrape_tool,
                self.search_tool,
            ],
            verbose=True,
            cache=True,
        )

    @agent
    def resume_strategist1(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_strategist"],
            llm=self.proposer1,
            function_calling_llm=self.tool_llm,
            tools=[
                self.file_read_tool,
                self.semantic_search_resume,
                self.scrape_tool,
                self.search_tool,
            ],
            verbose=True,
            cache=True,
        )

    @agent
    def resume_strategist2(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_strategist"],
            llm=self.proposer2,
            function_calling_llm=self.tool_llm,
            tools=[
                self.file_read_tool,
                self.semantic_search_resume,
                self.scrape_tool,
                self.search_tool,
            ],
            verbose=True,
            cache=True,
        )

    @agent
    def resume_strategist3(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_strategist"],
            llm=self.proposer3,
            function_calling_llm=self.tool_llm,
            tools=[
                self.file_read_tool,
                self.semantic_search_resume,
                self.scrape_tool,
                self.search_tool,
            ],
            verbose=True,
            cache=True,
        )

    @agent
    def aggregator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["aggregator"],
            llm=self.aggregator_llm,
            function_calling_llm=self.tool_llm,
            tools=[
                self.file_read_tool,
                self.semantic_search_resume,
            ],
            verbose=True,
            cache=True,
        )

    @agent
    def interview_preparer(self) -> Agent:
        return Agent(
            config=self.agents_config["interview_preparer"],
            llm=self.aggregator_llm,
            function_calling_llm=self.tool_llm,
            tools=[
                self.file_read_tool,
                self.semantic_search_resume,
                self.scrape_tool,
                self.search_tool,
            ],
            verbose=True,
            cache=True,
        )

    # @agent
    # def resume_validator(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["resume_validator"],
    #         llm=self.llm,
    #         function_calling_llm=self.tool_llm,
    #         tools=[
    #             self.file_read_tool,
    #             self.semantic_search_resume,
    #         ],
    #         verbose=True,
    #         cache=True,
    #     )

    # @agent
    # def resume_corrector(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["resume_corrector"],
    #         llm=self.llm,
    #         function_calling_llm=self.tool_llm,
    #         tools=[
    #             self.file_read_tool,
    #             self.semantic_search_resume,
    #         ],
    #         verbose=True,
    #         cache=True,
    #     )

    # @agent
    # def file_reader(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["file_reader"],
    #         llm=self.llm,
    #         function_calling_llm=self.tool_llm,
    #         tools=[
    #             self.file_read_tool,
    #             self.semantic_search_resume,
    #         ],
    #         verbose=True,
    #     )

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
    def resume_strategy_task1(self) -> Task:
        return Task(
            config=self.tasks_config["resume_strategy_task"],
            agent=self.resume_strategist1(),
            context=[
                self.research_task(),
                self.profile_task(),
            ],
            output_file="rockin_robin/files/tailored_resume1.md",
        )

    @task
    def resume_strategy_task2(self) -> Task:
        return Task(
            config=self.tasks_config["resume_strategy_task"],
            agent=self.resume_strategist2(),
            context=[
                self.research_task(),
                self.profile_task(),
            ],
            output_file="rockin_robin/files/tailored_resume2.md",
        )

    @task
    def resume_strategy_task3(self) -> Task:
        return Task(
            config=self.tasks_config["resume_strategy_task"],
            agent=self.resume_strategist3(),
            context=[
                self.research_task(),
                self.profile_task(),
            ],
            output_file="rockin_robin/files/tailored_resume3.md",
        )

    @task
    def aggregation_task(self) -> Task:
        return Task(
            config=self.tasks_config["aggregation_task"],
            agent=self.aggregator_agent(),
            context=[
                self.resume_strategy_task1(),
                self.resume_strategy_task2(),
                self.resume_strategy_task3(),
            ],
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
                self.aggregation_task(),
            ],
            output_file="rockin_robin/files/interview_materials.md",
        )

    # @task
    # def file_reading_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["file_reading_task"],
    #         agent=self.file_reader(),
    #         context=[
    #             self.resume_strategy_task(),
    #         ],
    #     )

    # @task
    # def resume_validation_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["resume_validation_task"],
    #         agent=self.resume_validator(),
    #         context=[self.resume_strategy_task(), self.file_reading_task()],
    #     )

    # @task
    # def resume_correction_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config["resume_correction_task"],
    #         agent=self.resume_strategist(),
    #         context=[
    #             self.research_task(),
    #             self.resume_strategy_task(),
    #         ],
    #         output_file="rockin_robin/files/tailored_resume.md",
    #     )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=2,
            process=Process.sequential,
            memory=True,
            cache=True,
            full_output=True,
        )
