"""
This module contains Serializers of models
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Task


class UserSerializer(serializers.ModelSerializer):
    """
    Serialize User Model
    """

    password = serializers.CharField(
        style={'input_type': 'password'})

    class Meta:
        """
        Specifying model and fields to be serialize.
        """

        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        write_only_fields = ('password', )


class TaskSerializer(serializers.ModelSerializer):
    """
    Serialize Task Model
    """

    link = serializers.SerializerMethodField()

    class Meta:
        """
        Specifying model and fields to be serialize.
        """
        model = Task
        fields = ['task_title', 'task_description', 'is_complete', 'task_category',
                  'start_date', 'completed_date', 'owner', 'link']
        read_only_fields = ('owner',)

    @staticmethod
    def get_link(task):
        """
        Message: Create reference for every task to view specifically.
        Parameters:
            task (Task): Task object
        Returns:
            Address of Task
        """
        return f'http://127.0.0.1:8000/tasks/{task.pk}'
