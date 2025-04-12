from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from datetime import datetime

# === Default email account (can be overridden per job) ===
DEFAULT_SENDER_EMAIL = "hazmatt.ai@gmail.com"
DEFAULT_SENDER_PW = "zjxtbtxeyiggclai"

# === JobStore backed by SQLite for persistence ===
jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///scheduled_emails.sqlite')
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()


def send_email(receiver_email: str,
               subject: str,
               message: str,
               html: bool = False,
               sender_email: str = DEFAULT_SENDER_EMAIL,
               sender_pw: str = DEFAULT_SENDER_PW):
    """
    Sends an email using Gmail's SMTP server.

    Args:
        receiver_email (str): Recipient's email address.
        subject (str): Email subject line.
        message (str): Email body (plain text or HTML).
        html (bool): If True, sends message as HTML. Defaults to False.
        sender_email (str): Sender's email address. Defaults to DEFAULT_SENDER_EMAIL.
        sender_pw (str): Sender's app password. Defaults to DEFAULT_SENDER_PW.
    """
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    mime_type = "html" if html else "plain"
    msg.attach(MIMEText(message, mime_type))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.ehlo(name="localhost")
            server.login(sender_email, sender_pw)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def schedule_email(run_time: datetime, **kwargs):
    """
    Schedule an email to be sent later.

    Args:
        run_time: datetime object specifying when to send the email
        kwargs: all arguments for send_email
    """
    scheduler.add_job(
        send_email,
        'date',
        run_date=run_time,
        kwargs=kwargs,
        id=f"{kwargs.get('receiver_email')}_{run_time.isoformat()}",
        replace_existing=True
    )
    print(f"📅 Email scheduled to {kwargs.get('receiver_email')} at {run_time}")


# === EXAMPLE USAGE ===
if __name__ == "__main__":
    # Example: send an email 1 minute from now
    from datetime import timedelta, datetime

    run_at = datetime.now() + timedelta(seconds=10)

    schedule_email(
        run_time=run_at,
        receiver_email="mattmuell297@gmail.com",
        subject="Scheduled Hello",
        message="This is a scheduled email from your Python script! 🎯",
        html=False,  # Optional: set True to send as HTML
        # sender_email="optional@gmail.com",  # Optional override
        # sender_pw="your-app-password"       # Optional override
    )

    while True:
        x = 4

