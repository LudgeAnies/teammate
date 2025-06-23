from djoser import email
from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage
from django.utils import timezone
from djoser import utils
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
import logging

logger = logging.getLogger(__name__)

class ActivationEmail(email.BaseEmailMessage):
    template_name = "account/email/activation.html"

    def send(self, to, *args, **kwargs):
        message = self.render()
        subject = self.subject
        from_email = self.from_email
        html_message = message
        # to = [to]
        # print(to)
        msg = EmailMessage(subject, html_message, from_email, to)
        msg.content_subtype = "html"
        msg.send()
        logger.info(f"Activation Email sent to console: {html_message}")  # логируем в консоль
        return

class ConfirmationEmail(email.BaseEmailMessage):
    template_name = "account/email/confirmation.html"

    def send(self, to, *args, **kwargs):
        message = self.render()
        subject = self.subject
        from_email = self.from_email
        html_message = message
        # to = [to]
        # print(to)
        msg = EmailMessage(subject, html_message, from_email, to)
        msg.content_subtype = "html"
        msg.send()
        logger.info(f"Confirmation Email sent to console: {html_message}")  # логируем в консоль
        return