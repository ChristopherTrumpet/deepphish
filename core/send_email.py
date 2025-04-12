import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

DEFAULT_SENDER_EMAIL = 'hazmatt.ai@gmail.com'
DEFAULT_SENDER_PW = 'zjxtbtxeyiggclai'


def send_email(receiver_email: str, subject: str, message: str,
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


send_email(
    receiver_email="mattmuell297@gmail.com",
    subject="Greetings from Python",
    message="<h1>This is an HTML email!</h1><p>Sent from Python 🎉</p>",
    html=True
)
