from src.rockin_robin.custom_tools.markdown_to_pdf import MarkdownToPDFTool
import click
from trogon import tui
from src.rockin_robin.crew import ResumeCustomizerCrew
from dotenv import load_dotenv

load_dotenv()


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
