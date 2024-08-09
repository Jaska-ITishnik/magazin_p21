# Create your tasks here

from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_to_email_task(subject, message, email):
    email = EmailMessage(subject, message, to=[email])
    email.content_subtype = 'html'
    email.send()
    return {"status": "KETTI", "email": email}