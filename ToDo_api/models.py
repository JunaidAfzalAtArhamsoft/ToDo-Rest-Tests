from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format('http://127.0.0.1:8000/api/password_reset/confirm/',
                                                   reset_password_token.key)
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


#
# class Person(User):
#
#     def tokens(self):
#         """
#         Message: Create the token for authenticated user.
#         """
#         token = RefreshToken.for_user(self)
#         return {
#             'refresh': str(token),
#             'access': str(token.access_token)
#         }
#

class Task(models.Model):
    task_title = models.CharField(max_length=100)
    task_description = models.TextField()
    is_complete = models.BooleanField(default=False)
    category = [
        ('Home_task', 'Home Task'),
        ('Office_task', 'Office Task'),
        ('MISC', 'Misc'),
    ]
    task_category = models.CharField(max_length=11, choices=category, blank=False)
    start_date = models.DateTimeField(default=datetime.now())
    completed_date = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Message: Show task title as default
        Parameters:
            self:
        Returns:
            task_title (str): Return task title
        """
        return self.task_title

    def get_absolute_url(self):
        return reverse('tasks/<int:pk>/', kwargs={'pk': self.pk})


