from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    phone = models.CharField(max_length=12, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Patient(models.Model):
    user = models.OneToOneField(User, related_name='patient', on_delete=models.CASCADE)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Doctor(models.Model):
    user = models.OneToOneField(User, related_name='doctor', on_delete=models.CASCADE)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.email


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )