import matplotlib.pyplot as plt
import pandas as pd
import os
import base64
from io import BytesIO
from datetime import datetime
import re
from data.db import DatabaseManager
import numpy as np

def columns_to_rows_loop(array_2d, column_indices):
  """Selects specific columns and makes them rows in the output using a loop."""
  if not array_2d or not array_2d[0]:
    return []

  num_rows_original = len(array_2d)
  num_cols_original = len(array_2d[0])
  output_array = []

  for col_index in column_indices:
    if 0 <= col_index < num_cols_original:
      new_row = [array_2d[i][col_index] for i in range(num_rows_original)]
      output_array.append(new_row)
    else:
      print(f"Warning: Column index {col_index} is out of bounds.")

  return output_array

def columns_to_rows_loop(array_2d, column_indices): 
    np.array(array_2d)

    modified = array_2d[:, column_indices]

    return modified.T

    
    

# --- Configuration & Sample Data ---
# IMPLEMENT DATA HERE FROM ACTUAL DATABASE
def get_phishing_data(company_id):
    """
    Provides sample data for the phishing test report.
    In a real scenario, this data would come from your testing platform or database.
    """
    db_manager = DatabaseManager()

    employees = db_manager.get_employees_by_company(company_id)
    print(employees) 
    return

    data = {
        'Employee Name': [
            'Alice Smith', 'Bob Johnson', 'Charlie Brown', 'Diana Prince',
            'Ethan Hunt', 'Fiona Glenanne', 'George Constanza', 'Hannah Abbott',
            'Ian Malcolm', 'Jane Doe'
        ],
        'Status': [
            'Clicked Link - Remediation Required', 'Reported Phish', 'Ignored', 'Clicked Link - Remediation Required',
            'Reported Phish', 'Reported Phish', 'Clicked Link - Remediation Complete', 'Ignored',
            'Clicked Link - Remediation Required', 'Reported Phish'
        ],
        'Department': [
            'Sales', 'Engineering', 'Marketing', 'Sales',
            'Engineering', 'Marketing', 'Sales', 'Engineering',
            'Marketing', 'Sales'
        ],
        'Reported Date': [
            None, '2025-04-10', None, None,
            '2025-04-11', '2025-04-10', '2025-04-12', None,
            None, '2025-04-11'
        ]
    }
    return pd.DataFrame(data)

# --- Chart Generation ---

def generate_status_pie_chart(df):
    """
    Generates a pie chart summarizing the phishing test statuses
    and returns it as a base64 encoded string.

    Args:
        df (pd.DataFrame): DataFrame containing the phishing test results.

    Returns:
        str: Base64 encoded PNG image string, or None if an error occurs.
    """
    try:
        status_counts = df['Status'].value_counts()

        fig, ax = plt.subplots(figsize=(8, 6)) # Create figure and axes objects
        wedges, texts, autotexts = ax.pie(
            status_counts,
            labels=status_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.85, # Distance of percentage labels from center
            labeldistance=1.1 # Distance of category labels from center
        )

        # Improve label appearance
        plt.setp(autotexts, size=10, weight="bold", color="white")
        plt.setp(texts, size=12)
        ax.set_title('Phishing Test Results Summary', fontsize=16, pad=20)

        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')

        # Save chart to a memory buffer
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight') # Use bbox_inches='tight'
        plt.close(fig)  # Close the figure to free memory
        buf.seek(0)

        # Encode buffer to base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        return image_base64

    except Exception as e:
        print(f"Error generating pie chart: {e}")
        return None

# --- Markdown Generation ---

def build_report_content_professional(data_df, chart_base64):
    """
    Builds a professional and well-styled Markdown report for phishing test results.
    
    Args:
        data_df (pd.DataFrame): The phishing test results.
        chart_base64 (str): Base64-encoded image of a chart visualization.

    Returns:
        str: Formatted Markdown report.
    """
    now = datetime.now()
    report_date_full = now.strftime("%B %d, %Y")
    report_generated = now.strftime("%Y-%m-%d %H:%M:%S")
    total_tested = len(data_df)

    if total_tested == 0:
        return "# Phishing Simulation Report\n\n**No data available to generate the report.**"

    # Summary metrics
    clicked = len(data_df[data_df['Status'].str.contains("Clicked Link", na=False)])
    reported = len(data_df[data_df['Status'] == 'Reported Phish'])
    ignored = len(data_df[data_df['Status'] == 'Ignored'])
    remediation_required = len(data_df[data_df['Status'] == 'Clicked Link - Remediation Required'])

    # Percentages
    clicked_pct = clicked / total_tested
    reported_pct = reported / total_tested
    ignored_pct = ignored / total_tested

    # Determine next quarter for recommendation
    current_quarter = (now.month - 1) // 3 + 1
    next_quarter = 1 if current_quarter == 4 else current_quarter + 1
    next_quarter_year = now.year if current_quarter < 4 else now.year + 1

    # --- Report Assembly ---
    md = []

    # --- Cover / Header ---
    md.append("# DeepPhish Simulation + Risk Assessment Report\n")
    md.append(f"**Assessment Date:** {report_date_full}  ")
    md.append(f"**Report Generated:** {report_generated}\n")
    md.append("---")

    # --- 1. Executive Summary ---
    md.append("## 1. Executive Summary\n")
    md.append(
        f"This report presents the results of a phishing simulation exercise conducted on **{report_date_full}**. "
        f"A total of **{total_tested}** employees were included in the test to evaluate their response to a simulated phishing threat.\n"
    )
    md.append(f"- Clicked the link: {clicked} employees (**{clicked_pct:.1%}**)\n"
              f"- Reported the phish: {reported} employees (**{reported_pct:.1%}**)\n"
              f"- Ignored the email: {ignored} employees (**{ignored_pct:.1%}**)\n"
              f"- Remediation needed: {remediation_required} employees\n")
    md.append("\nThis data highlights both areas of strength and potential risks within the organization’s current awareness levels.\n")

    # --- 2. Visualization ---
    md.append("## 2. Simulation Response Visualization\n")
    if chart_base64:
        md.append("Below is a graphical representation of employee responses during the simulation:\n")
        md.append(f"![Phishing response chart](data:image/png;base64,{chart_base64})\n")
    else:
        md.append("_Chart unavailable. Please ensure the visualization step was completed correctly._\n")

    # --- Page Break ---
    md.append('<div style="page-break-before: always;"></div>\n')

    # --- 3. Detailed Results Table ---
    md.append("## 3. Detailed Interaction Log\n")
    md.append("The following table contains a log of all participants and their corresponding actions during the simulation.\n")
    md.append(create_html_table_with_borders(data_df))
    md.append("\n")

    # --- Page Break (Optional) ---
    md.append('<div style="page-break-before: always;"></div>\n')

    # --- 4. Analysis & Recommendations ---
    md.append("## 4. Analysis & Strategic Recommendations\n")
    md.append(
        "This phishing simulation provides meaningful insights into the organization's readiness against social engineering threats. "
        "Key findings and actionable recommendations are outlined below:\n"
    )
    md.append("- **Targeted Remediation Training**  \n"
              f"  Provide mandatory training to the **{remediation_required}** employees who interacted with the phishing email. "
              "Focus on spotting red flags, verifying sender legitimacy, and best practices for email handling.\n")
    md.append("- **Positive Reinforcement & Recognition**  \n"
              f"  Acknowledge the **{reported}** employees who correctly reported the phishing attempt. Recognition can increase motivation and awareness across the team.\n")
    md.append("- **Technical Control Audit**  \n"
              "  Review the effectiveness of current email filtering, anti-spoofing protocols (DMARC, DKIM, SPF), and threat detection systems to reduce phishing exposure.\n")
    md.append(f"- **Ongoing Testing**  \n"
              f"  Plan the next simulation for **Q{next_quarter} {next_quarter_year}**. Iterative testing improves long-term resilience and tracks security awareness progress.\n")

    # --- Footer ---
    md.append("---")
    md.append("_Report compiled by the DeepPhish for the ML@Purdue Hackathon!_")

    return "\n".join(md)

def generate_individual_reports(output_dir: str = "individual_reports"):
    """
    Generates a personalized Markdown report file for each employee in the DataFrame.

    Args:
        data_df (pd.DataFrame): DataFrame containing employee phishing results.
                                Must include columns like 'Employee Name' and 'Status'.
        output_dir (str, optional): The directory where individual reports will be saved.
                                    Defaults to "individual_reports".

    Requires:
        - pandas library (pip install pandas)
    """
    print(f"\nGenerating individual employee reports in directory: '{output_dir}'...")

    data_df = get_phishing_data()

    # Create the output directory if it doesn't exist
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory '{output_dir}': {e}")
        return # Stop if directory cannot be created

    if 'Employee Name' not in data_df.columns or 'Status' not in data_df.columns:
        print("Error: DataFrame must contain 'Employee Name' and 'Status' columns.")
        return

    # --- Loop through each employee ---
    for index, row in data_df.iterrows():
        employee_name = row['Employee Name']
        status = row['Status']
        # Add other relevant fields if needed, e.g., row['Department']

        # Sanitize employee name for use in filename
        safe_filename_name = re.sub(r'[^\w\s-]', '', employee_name).strip().replace(' ', '_')
        if not safe_filename_name: # Handle cases where name becomes empty after sanitizing
            safe_filename_name = f"employee_{index}"
        filename = f"{safe_filename_name}_phishing_report.md"
        filepath = os.path.join(output_dir, filename)

        # --- Build Personalized Markdown Content ---
        md_content = []
        report_date = datetime.now().strftime("%B %d, %Y")

        md_content.append(f"# Personalized Phishing Simulation Results")
        md_content.append(f"**Date:** {report_date}")
        md_content.append(f"**Employee:** {employee_name}\n")
        # Optional: md_content.append(f"**Department:** {row.get('Department', 'N/A')}\n") # Safely get department
        md_content.append("---")

        md_content.append(f"Dear {employee_name.split()[0]},") # Use first name
        md_content.append("\nThis report summarizes your interaction during the recent phishing security simulation.\n")

        # --- Personalized Status and Recommendation ---
        md_content.append("## Your Result Summary\n")
        if "Clicked Link" in status:
            md_content.append(f"**Your Action:** You clicked the link in the simulated phishing email.")
            md_content.append(f"**Status:** `{status}`") # Show full status like 'Remediation Required'
            md_content.append("\n**Recommendation:** Clicking links in unexpected emails can expose sensitive data or install malware. We strongly recommend completing the assigned security awareness training module on identifying phishing attempts. Please reach out to IT Security if you have questions.")
            # Optional: Add specific training link here
            # md_content.append("\n[Link to Required Training Module](https://your-training-platform.com/phishing-module)")
        elif status == 'Reported Phish':
            md_content.append(f"**Your Action:** You correctly identified and reported the simulated phishing email.")
            md_content.append(f"**Status:** `{status}`")
            md_content.append("\n**Recommendation:** Excellent work! Reporting suspicious emails is crucial for protecting our organization. Your vigilance helps keep everyone safe. Thank you for following the correct procedure.")
        elif status == 'Ignored':
            md_content.append(f"**Your Action:** You did not interact with or report the simulated phishing email.")
            md_content.append(f"**Status:** `{status}`")
            md_content.append("\n**Recommendation:** While ignoring suspicious emails is better than clicking, the safest action is to report them using the official reporting channel (e.g., 'Report Phish' button or forwarding to security@yourcompany.com). This allows our security team to analyze potential threats.")
        else: # Handle any other statuses
            md_content.append(f"**Your Action:** Your interaction status was recorded as `{status}`.")
            md_content.append("\n**Recommendation:** Please review general security best practices regarding email safety. If you have questions about this status, contact IT Security.")

        md_content.append("\n---\n")

        # --- General Tips ---
        md_content.append("## General Security Reminders\n")
        md_content.append("* **Verify Senders:** Always check the sender's email address carefully.")
        md_content.append("* **Inspect Links:** Hover over links (without clicking!) to see the actual destination URL.")
        md_content.append("* **Beware Urgency:** Phishing emails often create a false sense of urgency.")
        md_content.append("* **Never Share Credentials:** Legitimate services will rarely ask for your password via email.")
        md_content.append("* **When in Doubt, Report:** Use the official reporting method if an email seems suspicious.\n")

        md_content.append("---\n")
        md_content.append("_This is an automated report. Please contact IT Security with any questions._")

        # --- Write the individual file ---
        try:
            with open(filepath, "w", encoding='utf-8') as f:
                f.write("\n".join(md_content))
            # Optional: print(f"Generated report for {employee_name} at {filepath}")
        except Exception as e:
            print(f"Error writing report for {employee_name} to '{filepath}': {e}")

    print(f"Finished generating {len(data_df)} individual reports.")

# Helper function assumed to exist (from previous script)
def create_markdown_table(df):
    # Placeholder: Replace with your actual table generation logic
    try:
        # Use pandas to_markdown for easy and well-formatted tables
        # Requires the 'tabulate' library (`pip install tabulate`)
        return df.to_markdown(index=False)
    except ImportError:
        print("Warning: 'tabulate' library not found for table generation.")
        # Basic fallback
        header = "| " + " | ".join(df.columns) + " |"
        separator = "|-" + "-|".join(['-' * len(col) for col in df.columns]) + "-|"
        body = "\n".join(["| " + " | ".join(map(str, row)) + " |" for row in df.itertuples(index=False)])
        return f"{header}\n{separator}\n{body}"
    except Exception as e:
        print(f"Error creating markdown table: {e}")
        return "Error generating table."

def create_html_table_with_borders(df):
    """
    Creates an HTML table with visible borders for PDF rendering.
    Args:
        df (pd.DataFrame): DataFrame to convert.
    Returns:
        str: HTML table with styling.
    """
    # Basic table style with borders and padding
    table_style = (
        'style="border-collapse: collapse; width: 100%;"'
    )
    th_td_style = (
        'style="border: 1px solid #000; padding: 6px; text-align: left;"'
    )

    html = [f'<table {table_style}>']

    # Header
    html.append("<thead><tr>")
    for column in df.columns:
        html.append(f'<th {th_td_style}>{column}</th>')
    html.append("</tr></thead>")

    # Body
    html.append("<tbody>")
    for _, row in df.iterrows():
        html.append("<tr>")
        for cell in row:
            html.append(f'<td {th_td_style}>{cell}</td>')
        html.append("</tr>")
    html.append("</tbody>")

    html.append("</table>")
    return "\n".join(html)

# --- Main Execution ---

def generate_report_file(filename="phishing_test_report.md"):
    """
    Generates the phishing report Markdown file.

    Args:
        filename (str, optional): The name for the output Markdown file.
                                   Defaults to "phishing_test_report.md".
    """
    print("Generating phishing report...")
    try:
        # 1. Get Data
        phishing_data = get_phishing_data()
        print(f"Loaded data for {len(phishing_data)} employees.")

        # 2. Generate Chart
        print("Generating status pie chart...")
        chart_data = generate_status_pie_chart(phishing_data)
        if chart_data:
            print("Chart generated successfully.")
        else:
            print("Failed to generate chart.")

        # 3. Build Markdown Content
        print("Building Markdown content...")
        report_markdown = build_report_content_professional(phishing_data, chart_data)

        # 4. Write to File
        print(f"Writing report to '{filename}'...")
        with open(filename, "w", encoding='utf-8') as f:
            f.write(report_markdown)

        print(f"\nReport '{filename}' created successfully!")
        print(f"File saved in: {os.path.abspath(filename)}")

    except ImportError as e:
         print(f"\nError: Missing required library. Please install it: pip install {e.name}")
    except Exception as e:
        print(f"\nAn error occurred during report generation: {e}")


def main():
    generate_report_file()
    generate_individual_reports()

if __name__ == "__main__":
    main()