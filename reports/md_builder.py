import matplotlib.pyplot as plt
import pandas as pd
import os
import base64
from io import BytesIO
from datetime import datetime

# --- Configuration & Sample Data ---

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

def create_markdown_table(df):
    """
    Converts a pandas DataFrame to a Markdown formatted table.

    Args:
        df (pd.DataFrame): The DataFrame to convert.

    Returns:
        str: A Markdown formatted table string.
    """
    # Use pandas to_markdown for easy and well-formatted tables
    # Requires the 'tabulate' library (`pip install tabulate`)
    try:
        return df.to_markdown(index=False)
    except ImportError:
        print("Warning: 'tabulate' library not found. Using basic markdown table.")
        print("Install it for better tables: pip install tabulate")
        # Fallback basic markdown generation
        header = "| " + " | ".join(df.columns) + " |"
        separator = "|-" + "-|".join(['-' * len(col) for col in df.columns]) + "-|"
        body = "\n".join(["| " + " | ".join(map(str, row)) + " |" for row in df.values])
        return f"{header}\n{separator}\n{body}"
    except Exception as e:
        print(f"Error creating markdown table: {e}")
        return "Error generating table."


def build_report_content(data_df, chart_base64):
    """
    Builds the full Markdown report string.

    Args:
        data_df (pd.DataFrame): The phishing test data.
        chart_base64 (str): Base64 encoded string of the pie chart image.

    Returns:
        str: The complete Markdown report content.
    """
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_tested = len(data_df)
    clicked = len(data_df[data_df['Status'].str.contains("Clicked Link", na=False)])
    reported = len(data_df[data_df['Status'] == 'Reported Phish'])
    ignored = len(data_df[data_df['Status'] == 'Ignored'])
    remediation_required = len(data_df[data_df['Status'] == 'Clicked Link - Remediation Required'])

    # --- Start Building Markdown ---
    markdown_content = []

    markdown_content.append(f"# Phishing Security Test Report")
    markdown_content.append(f"**Report Generated:** {report_date}\n")

    markdown_content.append("## 1. Executive Summary")
    markdown_content.append(
        f"This report summarizes the results of the recent simulated phishing campaign. "
        f"A total of **{total_tested}** employees were tested. "
        f"Key findings include **{clicked}** employees clicking the simulated phishing link "
        f"and **{reported}** employees reporting the email as suspicious. "
        f"Currently, **{remediation_required}** employees require follow-up remediation actions."
    )
    markdown_content.append("---\n") # Horizontal Rule

    # --- Visualization Section ---
    markdown_content.append("## 2. Overall Results Visualization")
    if chart_base64:
        markdown_content.append("The following chart provides a visual breakdown of employee interactions:")
        # Embed the base64 image directly into Markdown
        markdown_content.append(f"![Phishing Results Summary](data:image/png;base64,{chart_base64})\n")
    else:
        markdown_content.append("*Chart generation failed. Please check logs.*\n")

    markdown_content.append("---\n") # Horizontal Rule

    # --- Detailed Results Table ---
    markdown_content.append("## 3. Detailed Employee Results")
    markdown_content.append("The table below lists individual employee interactions and status:")
    markdown_content.append(create_markdown_table(data_df))
    markdown_content.append("\n") # Add space after table

    markdown_content.append("---\n") # Horizontal Rule

    # --- Recommendations Section ---
    markdown_content.append("## 4. Recommendations")
    markdown_content.append("Based on the results, the following actions are recommended:")
    markdown_content.append("* Conduct targeted security awareness training for employees who clicked the link, focusing on identifying phishing indicators.")
    markdown_content.append("* Acknowledge and commend employees who correctly reported the phishing attempt.")
    markdown_content.append("* Review and potentially enhance email filtering rules to better detect similar threats.")
    markdown_content.append("* Schedule follow-up phishing simulations to measure improvement over time.")
    markdown_content.append("\n")

    markdown_content.append("---\n")
    markdown_content.append("*End of Report*")

    return "\n".join(markdown_content)

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
        report_markdown = build_report_content(phishing_data, chart_data)

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
    # Ensure the 'tabulate' library is installed for optimal table formatting
    # pip install tabulate
    generate_report_file()
    # You can specify a different filename:
    # generate_report_file("Q2_Phishing_Results.md")

