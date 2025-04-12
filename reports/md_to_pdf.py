import csv
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section
import os

def convert_markdown_to_pdf(text: str):
  """Converts in-house markdown format to a pdf file to send to clients
  
  Args:
    text: Markdown text to be exported
  """
  pdf = MarkdownPdf(toc_level=2)
  pdf.add_section(Section(text))
  pdf.meta["title"] = "CyberSecurity Analysis Report"
  pdf.meta["author"] = "Pretext AI"

  rid = 10
  pdf.save(f"report-{rid}.pdf")

def convert_md_file_to_pdf(markdown_filepath, output_name, output_dir=""):
  with open(markdown_filepath, 'r', encoding='utf-8') as f:
    markdown_text = f.read()

  pdf = MarkdownPdf(toc_level=2)
  pdf.add_section(Section(markdown_text, toc=True))

  pdf.meta["title"] = "CyberSecurity Analysis Report"
  pdf.meta["author"] = "Pretext AI"

  if (output_dir):
    pdf.save(f"{output_dir}/{output_name}.pdf")
  else:
    pdf.save(f"{output_name}.pdf")

def import_csv(file: str):
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, file)
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            data.append(row)
    return data

def main():
  convert_md_file_to_pdf("../reports/phishing_test_report.md")

if __name__ == "__main__":
  main()