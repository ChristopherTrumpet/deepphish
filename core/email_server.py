import json
import logging

from fastapi import FastAPI, Request
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# === Default email account (can be overridden per job) ===
DEFAULT_SENDER_EMAIL = "hazmatt.ai@gmail.com"
DEFAULT_SENDER_PW = "dyluejusivgscksr"

# === JobStore backed by SQLite for persistence ===
app = FastAPI()
jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///scheduled_emails.sqlite')
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.info("starting log...")


def send_email(**kwargs):
    sender_email = kwargs.get("sender_email", DEFAULT_SENDER_EMAIL)
    sender_pw = kwargs.get("sender_pw", DEFAULT_SENDER_PW)

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = kwargs["receiver_email"]
    msg["Subject"] = kwargs["subject"]

    mime_type = "html" if kwargs.get("html", False) else "plain"
    msg.attach(MIMEText(kwargs["message"], mime_type))

    #try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.ehlo(name="localhost")
        server.login(DEFAULT_SENDER_EMAIL, DEFAULT_SENDER_PW)
        server.send_message(msg)
    print("Email sent successfully!")


class EmailJob(BaseModel):
    campaign_id: int
    receiver_email: str
    subject: str
    message: str
    send_time: str  # ISO format
    html: bool = False
    sender_email: str = None
    sender_pw: str = None


@app.post("/start_campaign")
# Example POST /start_campaign Payload
# [
#   {
#     "campaign_id": 42,
#     "receiver_email": "john@example.com",
#     "subject": "Kickoff!",
#     "message": "Welcome to our campaign",
#     "send_time": "2025-04-13T15:00:00",
#     "html": false
#   },
#   {
#     "campaign_id": 42,
#     "receiver_email": "jane@example.com",
#     "subject": "Kickoff!",
#     "message": "<b>Welcome to our campaign</b>",
#     "send_time": "2025-04-13T15:05:00",
#     "html": true
#   }
# ]
async def start_campaign(jobs: list[EmailJob]):
    logger.debug("Jobs received: %s", jobs)
    for job in jobs:
        scheduler.add_job(
            send_email,
            "date",
            run_date=job.send_time,
            kwargs=job.dict(),
            id=f"{job.campaign_id}_{job.receiver_email}_{job.send_time}"
        )
    return {"status": "scheduled", "jobs": len(jobs)}


@app.post("/cancel_campaign")
async def cancel_campaign(request: Request):
    body = await request.json()
    cid = body["campaign_id"]
    jobs = scheduler.get_jobs()
    cancelled = 0
    for job in jobs:
        if job.id.startswith(str(cid)):
            scheduler.remove_job(job.id)
            cancelled += 1
    return {"status": "cancelled", "jobs_removed": cancelled}
