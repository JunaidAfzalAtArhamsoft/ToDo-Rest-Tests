"""
This module contains url patterns for api to_do_api
"""

from django.urls import path
from . import views

APP_NAME = 'TODO_REST'
urlpatterns = [
    path('', views.hello, name='main_page'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('tasks/', views.TaskListCreateView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', views.TaskDetailUpdateDeleteView.as_view(), name='tasks-detail'),
]
