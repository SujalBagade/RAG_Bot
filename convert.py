from PyPDF2 import PdfReader
import re
import os

def convert_pdf_to_md(pdf_file, output_dir):
    """Converts a PDF file to a Markdown file.

    Args:
        pdf_file: The path to the PDF file.
        output_dir: The path to the output directory for Markdown files.
    """
    # Get the base name of the PDF file without extension.
    pdf_basename = os.path.splitext(os.path.basename(pdf_file))[0]
    
    # Generate the output Markdown file path with the same name as the PDF.
    md_file = os.path.join(output_dir, f"{pdf_basename}.md")

    # Open the PDF file.
    pdf_reader = PdfReader(pdf_file)

    # Create a Markdown writer.
    with open(md_file, "w", encoding="utf-8") as md_writer:
        # Iterate over the pages in the PDF file.
        for page in pdf_reader.pages:
            # Extract the text from the page.
            text = page.extract_text()

            # Convert the text to Markdown.
            markdown_text = re.sub(r"\n+", "\n\n", text)

            # Write the Markdown text to the file.
            md_writer.write(markdown_text)

def convert_all_pdfs_to_md(input_dir, output_dir):
    """Converts all PDF files in input directory to Markdown in output directory."""
    # Ensure output directory exists; create if not.
    os.makedirs(output_dir, exist_ok=True)

    # Loop through PDF files in the input directory.
    for pdf_file in os.listdir(input_dir):
        if pdf_file.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, pdf_file)
            convert_pdf_to_md(pdf_path, output_dir)
            print(f"Converted {pdf_file} to Markdown.")

if __name__ == "__main__":
    input_directory = "data/input_pdf"
    output_directory = "data/files"
    convert_all_pdfs_to_md(input_directory, output_directory)
