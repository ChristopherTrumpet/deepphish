import requests
import sys
from datetime import datetime, timedelta
sys.path.append('../llm')
import llm
import link

url = "http://127.0.0.1:8000/start_campaign"

# Dummy employee list
employees = [
    {"name": "Alice Smith", "email": "mattmuell297@gmail.com"},
    {"name": "Alice Smith", "email": "gutobutkewitsch@gmail.com"}
]

# Base schedule time
base_time = datetime.now()

# Campaign ID
campaign_id = 42

# Generate email jobs
email_jobs = []

for i, employee in enumerate(employees):

    subject, body = llm.get_phish_email("hard", "chris trumpet works at envision center at purdue university and has trouble with outlook account")
    body.replace("<LINK>", link.get_unique_url(employees[0]["email"].split('@')[0]))

    email_jobs.append({
        "campaign_id": campaign_id,
        "receiver_email": employee["email"],
        "subject": subject,
        "message": body,
        "send_time": (base_time + timedelta(seconds=(i+1)*10)).isoformat(),
        "html": True
    })

# Optional: pretty print
import json
print(json.dumps(email_jobs, indent=2))

response = requests.post(url, json=email_jobs)

print("Response Status:", response.status_code)
print("Response Body:", response.json())
