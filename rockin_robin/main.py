from crewai import Agent, Task, Crew
from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  MDXSearchTool,
  SerperDevTool
)
from custom_tools.markdown_to_pdf import MarkdownToPDFTool

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
read_resume = FileReadTool(file_path='joshua_oliphant_resume.md')
semantic_search_resume = MDXSearchTool(mdx='joshua_oliphant_resume.md')
markdown_to_pdf_converter_tool = MarkdownToPDFTool(markdown_file_path='tailored_resume.md')
read_tailored_resume = FileReadTool(file_path='tailored_resume.md')


# Agent 1: Researcher
researcher = Agent(
    role="Tech Job Researcher",
    goal="Make sure to do amazing analysis on "
         "job posting to help job applicants",
    tools=[scrape_tool, search_tool],
    verbose=True,
    backstory=(
        "As a Job Researcher, your prowess in "
        "navigating and extracting critical "
        "information from job postings is unmatched."
        "Your skills help pinpoint the necessary "
        "qualifications and skills sought "
        "by employers, forming the foundation for "
        "effective application tailoring."
    )
)

# Agent 2: Profiler
profiler = Agent(
    role="Personal Profiler for Engineers",
    goal="Do increditble research on job applicants "
         "to help them stand out in the job market",
    tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Equipped with analytical prowess, you dissect "
        "and synthesize information "
        "from diverse sources to craft comprehensive "
        "personal and professional profiles, laying the "
        "groundwork for personalized resume enhancements."
    )
)

# Agent 3: Resume Strategist
resume_strategist = Agent(
    role="Resume Strategist for Engineers",
    goal="Find all the best ways to make a "
         "resume stand out in the job market.",
    tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "With a strategic mind and an eye for detail, you "
        "excel at refining resumes to highlight the most "
        "relevant skills and experiences, ensuring they "
        "resonate perfectly with the job's requirements."
    )
)

# Agent 4: Interview Preparer
interview_preparer = Agent(
    role="Engineering Interview Preparer",
    goal="Create interview questions and talking points "
         "based on the resume and job requirements",
    tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Your role is crucial in anticipating the dynamics of "
        "interviews. With your ability to formulate key questions "
        "and talking points, you prepare candidates for success, "
        "ensuring they can confidently address all aspects of the "
        "job they are applying for."
    )
)

# Agent 5: Markdown to PDF Converter
markdown_to_pdf_converter = Agent(
    role="Markdown to PDF Converter",
    goal="Take a markdown file and convert it to a PDF file",
    tools=[read_tailored_resume, markdown_to_pdf_converter_tool],
    verbose=True,
    backstory=(
        """Your role is to convert the tailored resume from markdown format to PDF format."""
    )
)

# Task for Researcher Agent: Extract Job Requirements
research_task = Task(
    description=(
        "Analyze the job posting URL provided ({job_posting_url}) "
        "to extract key skills, experiences, and qualifications "
        "required. Use the tools to gather content and identify "
        "and categorize the requirements."
    ),
    expected_output=(
        "A structured list of job requirements, including necessary "
        "skills, qualifications, and experiences."
    ),
    agent=researcher,
    async_execution=True
)

# Task for Profiler Agent: Compile Comprehensive Profile
profile_task = Task(
    description=(
        "Compile a detailed personal and professional profile "
        "using the GitHub ({github_url}) URLs, and personal write-up "
        "({personal_writeup}). Utilize tools to extract and "
        "synthesize information from these sources."
    ),
    expected_output=(
        "A comprehensive profile document that includes skills, "
        "project experiences, contributions, interests, and "
        "communication style."
    ),
    agent=profiler,
    async_execution=True
)

# Task for Resume Strategist Agent: Align Resume with Job Requirements
resume_strategy_task = Task(
    description=(
        "Using the profile and job requirements obtained from "
        "previous tasks, tailor the resume to highlight the most "
        "relevant areas. Employ tools to adjust and enhance the "
        "resume content. Make sure this is the best resume even but "
        "don't make up any information. Update every section, "
        "inlcuding the initial summary, work experience, skills, "
        "and education. All to better reflrect the candidates "
        "abilities and how it matches the job posting. The final "
        "output should be a complete resume. Any changes to style, "
        "font, spacing, emphasis, etc., should be reflected throughout the document."
    ),
    expected_output=(
        "An updated resume that effectively highlights the candidate's "
        "qualifications and experiences relevant to the job. Only the "
        "resume should be outputted, not any part of the conversation or other information."
    ),
    output_file="tailored_resume.md",
    context=[research_task, profile_task],
    agent=resume_strategist
)

# Task for Interview Preparer Agent: Develop Interview Materials
interview_preparation_task = Task(
    description=(
        "Create a set of potential interview questions and talking "
        "points based on the tailored resume and job requirements. "
        "Utilize tools to generate relevant questions and discussion "
        "points. Make sure to use these question and talking points to "
        "help the candiadte highlight the main points of the resume "
        "and how it matches the job posting."
    ),
    expected_output=(
        "A document containing key questions and talking points "
        "that the candidate should prepare for the initial interview."
    ),
    output_file="interview_materials.md",
    context=[research_task, profile_task, resume_strategy_task],
    agent=interview_preparer
)

# Task for Markdown to PDF Converter Agent: Convert Tailored Resume to PDF
markdown_to_pdf_task = Task(
    description=(
        """Convert the tailored resume from markdown format to PDF format."""
    ),
    expected_output=(
        """A PDF version of the tailored resume. Only the resume should be converted to PDF,
        not any part of the conversation or other information."""
    ),
    output_file="tailored_resume.pdf",
    context=[resume_strategy_task],
    agent=markdown_to_pdf_converter
)

job_application_crew = Crew(
    agents=[researcher,
            profiler,
            resume_strategist,
            interview_preparer,
            markdown_to_pdf_converter],

    tasks=[research_task,
           profile_task,
           resume_strategy_task,
           interview_preparation_task,
           markdown_to_pdf_task],

    verbose=True
)

job_application_inputs = {
    'job_posting_url': 'https://jobs.smartrecruiters.com/ServiceNow/743999977750493-senior-systems-engineer',
    'github_url': 'https://github.com/JoshuaOliphant',
    'personal_writeup': """Joshua is an experienced generalist software engineer.
    He started his career as a backend Java developer, but has since transitioned
    to DevOps and Site Reliability Engineering. He has a strong interest in automation,
    Kubernetes, platform engineering, and cloud technologies. Joshua is passionate 
    about learning to apply AI to solve real-world problems and is currently exploring
    AI agents with Python and CrewAI. He is seeking a role that allows him to leverage
    his diverse skill set and contribute to innovative projects.
    """
}

result = job_application_crew.kickoff(inputs=job_application_inputs)
