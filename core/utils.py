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

def import_csv(file: str):
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, file)
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            data.append(row)
    return data