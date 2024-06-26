from rockin_robin.crew.utils.markdown_to_pdf import MarkdownToPDF
import click
from trogon import tui
from rockin_robin.crew.crew import ResumeCustomizerCrew
from rockin_robin import create_app

app = create_app()


@tui()
@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--job_posting_url",
    "-j",
    help="The URL of the job posting to extract requirements.",
)
@click.option(
    "--github_url", "-g", help="The GitHub URL of the candidate for profiling."
)
@click.option(
    "--personal_writeup",
    "-p",
    help="The personal write-up of the candidate for profiling.",
)
@click.option(
    "--resume_file_path",
    "-r",
    help="The path to the resume file to be customized.",
)
def prepare_resume(job_posting_url, github_url, personal_writeup, resume_file_path):
    job_application_inputs = {
        "job_posting_url": job_posting_url,
        "github_url": github_url,
        "personal_writeup": personal_writeup,
        "resume_file_path": resume_file_path,
    }
    ResumeCustomizerCrew().crew().kickoff(inputs=job_application_inputs)
    tool = MarkdownToPDF(markdown_file_path="tailored_resume.md")
    tool._run()


@cli.command()
def run_flask():
    """Run the Flask development server."""
    app.run(debug=True)


if __name__ == "__main__":
    cli()
