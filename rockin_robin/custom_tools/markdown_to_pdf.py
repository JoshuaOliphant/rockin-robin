from crewai_tools import BaseTool
import pypandoc

    
class MarkdownToPDFTool(BaseTool):
    name: str = "MarkdownToPDFTool"
    description: str = "Converts markdown files to PDF using pypandoc."
    markdown_file_path: str = None

    def _run(self, markdown_file_path: str) -> str:
        # Define the output PDF file path
        pdf_file_path = markdown_file_path.replace('.md', '.pdf')

        # Convert markdown file to PDF and save it
        pypandoc.convert_file(markdown_file_path, 'pdf', outputfile=pdf_file_path)

        return f"PDF saved to {pdf_file_path}"


# Example usage
if __name__ == "__main__":
    tool = MarkdownToPDFTool()
    markdown_file_path = "tailored_resume.md"  # Replace with your markdown file path
    result = tool._run(markdown_file_path)
    print(result)