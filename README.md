# Rockin' Robin

This is a job application enhancement system that uses CrewAI agents to customize
a job resume and provide interview talking points, given a resume and a link to
a job description.

## Requirements

- [Serper](https://serper.dev/) environment variable `SERPER_API_KEY`
- OpenAI environment variable `OPENAI_API_KEY`
- OpenAI model name environment variable `OPENAI_MODEL_NAME`
- pandoc, if using mac then `brew install pandoc`
- latex, if using mac then `brew install mactex`
- Poetry, [installation](https://python-poetry.org/docs/#installation)

## Command Line Usage

This project uses the Click and Trogon libraries to provide a command line
interface.

```bash
poetry run rockin_robin --help   
Usage: rockin_robin [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  prepare-resume
  run-flask       Run the Flask development server.
  tui             Open Textual TUI.
```

## CrewAI Features

**Agents:**

- Researcher: Analyzes job postings to extract key requirements.
- Profiler: Compiles comprehensive profiles of job applicants.
- Resume Strategist: Aligns resumes with job requirements.
- Interview Preparer: Develops interview materials based on resumes and job requirements.
  
**Tasks:**

- Extract Job Requirements
- Compile Comprehensive Profile
- Align Resume with Job Requirements
- Develop Interview Materials

**Tools Used:**

ScrapeWebsiteTool, MDXSearchTool, FileReadTool, SerperDevTool
