import matplotlib.pyplot as plt
import pandas as pd
import os
import base64
from io import BytesIO
from datetime import datetime

# --- Configuration & Sample Data ---
# IMPLEMENT DATA HERE FROM ACTUAL DATABASE
def get_phishing_data():
    """
    Provides sample data for the phishing test report.
    In a real scenario, this data would come from your testing platform or database.
    """
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

if __name__ == "__main__":
    generate_report_file()