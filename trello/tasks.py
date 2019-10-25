from celery import shared_task
from django.core.mail import send_mail

@shared_task
def invite_member(subject,message,email_from,recipient_list,html_message):
    send_mail(subject, message, email_from, recipient_list, html_message=html_message)

