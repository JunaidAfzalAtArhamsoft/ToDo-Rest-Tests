""" Configuring app """

from django.apps import AppConfig


class TodoApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'to_do_api'
