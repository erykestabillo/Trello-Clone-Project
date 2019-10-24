from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import shared_task
from .email import send_feedback_email
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = get_task_logger(__name__)


@shared_task
def invite_member(subject,message,email_from,recipient_list,html_message):
    logger.info("Email sent")
    return send_mail( subject, message, email_from, recipient_list, html_message=html_message)