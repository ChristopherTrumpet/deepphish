from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

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