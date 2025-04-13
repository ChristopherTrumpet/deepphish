import requests
import sys
from datetime import datetime, timedelta
sys.path.append('../llm')
import llm
import link

url = "http://127.0.0.1:8000/start_campaign"

def start_campaign(campaign, employees):
    # Base schedule time
    base_time = datetime.now()

    # Campaign ID
    campaign_id = campaign.campaign_id

    # Generate email jobs
    email_jobs = []
    i = 0

    for employee in employees:

        risk_text = employee.risk_text
        difficulty = "medium" # Default difficulty
        if risk_text == "low":
            difficulty = "hard"
        elif risk_text == "medium":
            difficulty = "medium"
        elif risk_text == "high":
            difficulty = "easy"

        name = employee.name
        department = employee.department
        company_name = campaign.company_name

        input_str = f"{name} works in {department} at {company_name} and has trouble with their outlook account"

        subject, body = llm.get_phish_email(difficulty, input_str)
        body = body.replace("<LINK>", link.get_unique_url(employees.email.split('@')[0]))

        print(body)

        i = i + 1

        email_jobs.append({
            "campaign_id": campaign_id,
            "receiver_email": employee.email,
            "subject": subject,
            "message": body,
            "send_time": (base_time + timedelta(seconds=(i)*5)).isoformat(),
            "html": True
        })

    # Optional: pretty print
    import json
    #print(json.dumps(email_jobs, indent=2))
    import time
    time.sleep(3)

    response = requests.post(url, json=email_jobs)

    print("Response Status:", response.status_code)
    print("Response Body:", response.json())
