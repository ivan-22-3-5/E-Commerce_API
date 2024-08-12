import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from celery import Celery
from jinja2 import Environment, FileSystemLoader

from src.config import settings

celery = Celery("celery", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BACKEND_URL)


def send_email(username: str, link: str, email_address: str, subject: str, template_name: str):
    env = Environment(loader=FileSystemLoader('src/html_templates'))
    template = env.get_template(template_name)
    html_content = template.render(username=username, link=link)

    msg = MIMEMultipart()
    msg['From'] = settings.SMTP_MAIL
    msg['To'] = email_address
    msg['Subject'] = subject

    msg.attach(MIMEText(html_content, 'html'))

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg)


@celery.task
def send_password_recovery_email(username, link, email_address):
    send_email(username, link, email_address, subject="Password recovery", template_name="password_recovery.html")


@celery.task
def send_email_confirmation_email(username, link, email_address):
    send_email(username, link, email_address, subject="Email confirmation", template_name="email_confirmation.html")
