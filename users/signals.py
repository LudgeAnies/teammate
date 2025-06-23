from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.models import EmailAddress
from .tasks import send_confirmation_email

@receiver(post_save, sender=EmailAddress)
def email_address_changed(sender, instance, created, **kwargs):
    if created and instance.email and not instance.verified:
        send_confirmation_email.delay(instance.id)