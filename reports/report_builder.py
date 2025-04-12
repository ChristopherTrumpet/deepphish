import os
import md_builder
import md_to_pdf

def main():
    md_builder.generate_report_file()
    md_to_pdf.convert_md_file_to_pdf("phishing_test_report.md")
    print("PDF File saved")

if __name__ == "__main__":
    main()