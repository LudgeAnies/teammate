from django.core.mail import send_mail
from django.template.loader import render_to_string # рендер HTML-шаблона
from django.utils.html import strip_tags # HTML to plain text
from celery import shared_task
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC, EmailAddress
from allauth.account.forms import ResetPasswordForm
from allauth.account.utils import user_pk_to_url_str
from allauth.account.adapter import get_adapter
from django.contrib.sites.shortcuts import get_current_site # получение текущего сайта
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from smtplib import SMTPException

from django.contrib.sites.models import Site

@shared_task(bind=True, max_retries=3)
def send_confirmation_email(self, email_address_id):
    try:
        email_address = EmailAddress.objects.get(id=email_address_id)
        user = email_address.user
        email = email_address.email

        confirmation = EmailConfirmation.create(email_address)
        key = EmailConfirmationHMAC(confirmation).key

        #current_site = get_current_site(none)
        current_site = Site.objects.get_current()
        activate_url = reverse("account_confirm_email", kwargs={"key": key})

        context = {
            "user": user,
            "activate_url": f"http://{current_site.domain}{activate_url}", # заменить потом на https
            "current_site": current_site,
        }

        subject = f"Подтвердите ваш email на {current_site.name}"
        html_message = render_to_string(
            "account/email/email_confirmation_message.html",
            context
        )
        plain_message = strip_tags(html_message)

        send_mail(subject, plain_message, None, [email], html_message=html_message)

    except (ObjectDoesNotExist, SMTPException) as e:
        retry_count = self.request.retries
        countdown = [5, 10, 15][retry_count] if retry_count < 3 else 15
        raise self.retry(exc=e, countdown=countdown, max_retries=3)

@shared_task(bind=True, max_retries=3)
def send_password_reset_email(self, email):
    try:
        adapter = get_adapter()
        form = ResetPasswordForm(data={'email': email})
        if form.is_valid():
            email = form.cleaned_data['email']
            users = form.get_users(email)

            for user in users:
                current_site = get_current_site(None)
                token = adapter.generate_password_reset_token(user)
                path = reverse(
                    "account_reset_password_from_key",
                    kwargs={
                        "uidb36": user_pk_to_url_str(user),
                        "key": token,
                    },
                )
                reset_url = f"https://{current_site.domain}{path}"

                context = {
                    "user": user,
                    "password_reset_url": reset_url,
                    "current_site": current_site,
                }

                subject = f"Сброс пароля на {current_site.name}"
                html_message = render_to_string(
                    "account/email/password_reset_message.html",
                    context
                )
                plain_message = strip_tags(html_message)

                send_mail(subject, plain_message, None, [email], html_message=html_message)

    except (ObjectDoesNotExist, SMTPException) as e:
        retry_count = self.request.retries
        countdown = [5, 10, 15][retry_count] if retry_count < 3 else 15
        raise self.retry(exc=e, countdown=countdown, max_retries=3)

# НАПИСАТЬ СОБЫТИЕ ДЛЯ УВЕДОМЛЕНИЙ