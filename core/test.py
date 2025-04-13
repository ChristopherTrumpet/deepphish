import requests
from datetime import datetime, timedelta
import llm.llm


url = "http://127.0.0.1:8000/start_campaign"

# Dummy employee list
employees = [
    {"name": "Alice Smith", "email": "mattmuell297@gmail.com"},
    {"name": "Bob Johnson", "email": "mattmuell297@gmail.com"},
    {"name": "Carol Davis", "email": "mattmuell297@gmail.com"},
]

# Base schedule time
base_time = datetime(2025, 4, 13, 15, 0, 0)

# Campaign ID
campaign_id = 42

# Generate email jobs
email_jobs = []

for i, employee in enumerate(employees):
    email_jobs.append({
        "campaign_id": campaign_id,
        "receiver_email": employee["email"],
        "subject": "Kickoff!",
        "message": f"<b>Welcome, {employee['name']}!</b>\n" + llm.get_phish_email(),
        "send_time": (base_time + timedelta(seconds=i*10)).isoformat(),
        "html": True
    })

# Optional: pretty print
import json
print(json.dumps(email_jobs, indent=2))

response = requests.post(url, json=email_jobs)

print("Response Status:", response.status_code)
print("Response Body:", response.json())
