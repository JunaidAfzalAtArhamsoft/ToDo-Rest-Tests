"""
This module contains Definitions of models
"""
from datetime import datetime
from django_rest_passwordreset.signals import reset_password_token_created
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver
from django.urls import reverse
from django.db import models


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs) -> None:
    """
    Message: Send Password reset link to user email.
    Parameters:
        sender: Sender Name
        instance:
        reset_password_token:
    Returns:
        None
    """

    url = 'http://127.0.0.1:8000/api/password_reset/confirm/'
    email_plaintext_message = f"""{url}?token={reset_password_token.key}"
              \ninstance = {instance}
              \nsender = {sender}\n
              \nargs = {args}\n 
              \nkwargs = {kwargs}
              """

    send_mail(
        subject="Password Reset for Task Management System",
        message=email_plaintext_message,
        from_email="Junaid Afzal",
        recipient_list=[reset_password_token.user.email]
    )


class Task(models.Model):
    """
    Creating model for Task
    """
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
    completed_date = models.DateTimeField(blank=True, null=True, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Message: Show task title as default
        Parameters:
            self:
        Returns:
            task_title (str): Return task title
        """
        return str(self.task_title)

    def get_absolute_url(self) -> reverse:
        """
        Return url for specific task
        """
        return reverse('tasks/<int:pk>/', kwargs={'pk': self.pk})

    class Meta:  # pylint: disable=R0903
        """
        Specifying Task Order
        """

        ordering = ('pk',)
