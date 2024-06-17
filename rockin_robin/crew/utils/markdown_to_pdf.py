import pypandoc
import os


class MarkdownToPDF:
    name: str = "MarkdownToPDF"
    description: str = "Converts markdown files to PDF using pypandoc."
    markdown_file_path: str = None

    def use(self) -> str:
        # Define the base output PDF file path
        base_pdf_file_path = self.markdown_file_path.replace(".md", ".pdf")
        pdf_file_path = base_pdf_file_path

        # Check if the file exists and modify the path to make it unique
        counter = 1
        while os.path.exists(pdf_file_path):
            pdf_file_path = base_pdf_file_path.replace(".pdf", f"_{counter}.pdf")
            counter += 1

        # Convert markdown file to PDF and save it
        pypandoc.convert_file(
            source_file=self.markdown_file_path,
            to="pdf",
            format="markdown",
            outputfile=pdf_file_path,
        )

        return f"PDF saved to {pdf_file_path}"


# Example usage
if __name__ == "__main__":
    tool = MarkdownToPDF(markdown_file_path="rockin_robin/files/tailored_resume.md")
    result = tool.use()
    print(result)
