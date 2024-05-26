from src.rockin_robin.custom_tools.markdown_to_pdf import MarkdownToPDFTool
import click
from trogon import tui
from src.rockin_robin.crew import ResumeCustomizerCrew
from dotenv import load_dotenv

load_dotenv()

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


@tui()
@click.group()
def cli():
    pass


@cli.command()
@click.option('--job_posting_url', '-j', help='The URL of the job posting to extract requirements.')
@click.option('--github_url', '-g', help='The GitHub URL of the candidate for profiling.')
@click.option('--personal_writeup', '-p', help='The personal write-up of the candidate for profiling.')
def prepare_resume(job_posting_url, github_url, personal_writeup):
    job_application_inputs = {
        'job_posting_url': job_posting_url,
        'github_url': github_url,
        'personal_writeup': personal_writeup
    }
    ResumeCustomizerCrew().crew().kickoff(inputs=job_application_inputs)
    tool = MarkdownToPDFTool(markdown_file_path="tailored_resume.md")
    tool._run()


if __name__ == '__main__':
    cli()
