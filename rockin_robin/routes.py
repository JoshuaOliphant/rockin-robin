from flask import Blueprint, render_template, request, send_from_directory, current_app
from rockin_robin.crew.crew import ResumeCustomizerCrew
from rockin_robin.crew.custom_tools.markdown_to_pdf import MarkdownToPDFTool
import os
import logfire

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/process", methods=["POST"])
def process():
    job_posting_url = request.form.get("job_posting_url")
    github_url = request.form.get("github_url")
    personal_writeup = request.form.get("personal_writeup")
    resume_file_path = request.form.get("resume_file_path")

    job_application_inputs = {
        "job_posting_url": job_posting_url,
        "github_url": github_url,
        "personal_writeup": personal_writeup,
        "resume_file_path": resume_file_path,
    }
    ResumeCustomizerCrew(resume_file_path=resume_file_path).crew().kickoff(
        inputs=job_application_inputs
    )
    tool = MarkdownToPDFTool(markdown_file_path="rockin_robin/files/tailored_resume.md")
    tool._run()

    files_dir = os.path.join(current_app.root_path, "files")
    resume_path = os.path.join(files_dir, "tailored_resume.md")
    interview_path = os.path.join(files_dir, "interview_materials.md")

    # Ensure the directory exists
    os.makedirs(files_dir, exist_ok=True)

    # Write results to files
    with open(resume_path, "r") as f:
        updated_resume = f.read()

    with open(interview_path, "r") as f:
        interview_prep = f.read()

    return render_template(
        "results.html",
        updated_resume=updated_resume,
        interview_prep=interview_prep,
        resume_filename="tailored_resume.md",
        interview_filename="interview_materials.md",
    )


@main.route("/download/<filename>")
def download_file(filename):
    files_dir = os.path.join(current_app.root_path, "files")
    logfire.info(files_dir)
    return send_from_directory(directory=files_dir, path=filename)
