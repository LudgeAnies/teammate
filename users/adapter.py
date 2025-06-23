from allauth.account.adapter import DefaultAccountAdapter
from .tasks import send_password_reset_email, send_confirmation_email

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        if template_prefix in ['account/email/password_reset', 'account/email/email_confirmation']:
            send_password_reset_email.delay(email)
        else:
            super().send_mail(template_prefix, email, context)

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        user = emailconfirmation.email_address.user
        if user.is_superuser:
            emailconfirmation.confirm(request)
            return
        super().send_confirmation_mail(request, emailconfirmation, signup)