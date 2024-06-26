from flask import Blueprint, render_template, request, send_from_directory, current_app
from rockin_robin.crew.crew import ResumeCustomizerCrew
from rockin_robin.crew.utils.markdown_to_pdf import MarkdownToPDF
import os
import html

main = Blueprint("main", __name__)


def sanitize_input(input_string):
    if input_string is None:
        return ""
    # Escape HTML characters to prevent XSS attacks
    sanitized_string = html.escape(input_string)
    return sanitized_string


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/process", methods=["POST"])
def process():
    job_posting_url = sanitize_input(request.form.get("job_posting_url"))
    github_url = sanitize_input(request.form.get("github_url"))
    personal_writeup = sanitize_input(request.form.get("personal_writeup"))
    resume_file_path = sanitize_input(request.form.get("resume_file_path"))

    job_application_inputs = {
        "job_posting_url": job_posting_url,
        "github_url": github_url,
        "personal_writeup": personal_writeup,
        "resume_file_path": resume_file_path,
    }

    ResumeCustomizerCrew(resume_file_path=resume_file_path).crew().kickoff(
        inputs=job_application_inputs
    )

    files_dir = os.path.join(current_app.root_path, "files")
    resume_path = os.path.join(files_dir, "tailored_resume.md")
    interview_path = os.path.join(files_dir, "interview_materials.md")

    remove_delimiters_file(resume_path)

    markdown_to_pdf = MarkdownToPDF(markdown_file_path=resume_path)
    markdown_to_pdf.use()

    # Ensure the directory exists
    os.makedirs(files_dir, exist_ok=True)

    # Check if files exist before reading
    if os.path.exists(resume_path):
        with open(resume_path, "r") as f:
            updated_resume = f.read()
    else:
        updated_resume = "File not found"

    if os.path.exists(interview_path):
        with open(interview_path, "r") as f:
            interview_prep = f.read()
    else:
        interview_prep = "File not found"

    return render_template(
        "results.html",
        updated_resume=updated_resume,
        interview_prep=interview_prep,
        resume_filename="tailored_resume.md",
        interview_filename="interview_materials.md",
    )


def remove_delimiters_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Remove markdown delimiters from the first line if it exists
    if lines[0].strip() == "```markdown":
        lines = lines[1:]

    # Remove markdown delimiters from the last line if it exists
    if lines[-1].strip() == "```":
        lines = lines[:-1]

    with open(file_path, "w") as file:
        file.writelines(lines)


@main.route("/download/<filename>")
def download_file(filename):
    files_dir = os.path.join(current_app.root_path, "files")
    return send_from_directory(directory=files_dir, path=filename)
