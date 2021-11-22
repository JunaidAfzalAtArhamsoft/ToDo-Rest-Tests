from django.urls import path
from . import views

app_name = 'ToDo_REST'
urlpatterns = [
    path('', views.hello, name='main_page'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('tasks/', views.TaskListCreateView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', views.TaskDetailUpdateDeleteView.as_view(), name='tasks-detail'),
    # path('my-login/', views.LoginApiView.as_view(), name='login_api')
    # path('forgot-password/<token>/', views.send, name='forgot_password'),
]
