from django.urls import path
from . import views

app_name = 'ToDo_REST'
urlpatterns = [
    path('', views.hello, name='main_page'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('tasks/', views.TaskListCreateView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', views.TaskDetailUpdateDeleteView.as_view(), name='tasks-detail'),
    # path('login/', views.LoginApiView, name='login_api')
    # path('forgot-password/<token>/', views.send, name='forgot_password'),
]
