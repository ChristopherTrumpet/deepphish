import os
import md_builder
import md_to_pdf

def main_report():
    md_builder.main()
    md_to_pdf.convert_md_file_to_pdf("phishing_test_report.md", "main_report")

    for filename in os.listdir("individual_reports"):
        file_path = os.path.join("individual_reports", filename)
        if os.path.isfile(file_path):
            md_to_pdf.convert_md_file_to_pdf(file_path, f"employee_{filename}", "individual_reports")

    print("PDF(s) File saved")

if __name__ == "__main__":
    main_report()