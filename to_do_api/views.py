"""
This module contains Apis
"""
import datetime

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import CreateAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView, DestroyAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.backends import TokenBackend


from .serializers import UserSerializer, TaskSerializer
from .models import Task


def hello(request) -> HttpResponse:
    """
    Show Main Page
    """
    return HttpResponse(f'<h1>hello {request.META.get("PATH")}</h1>')


def get_tasks() -> Task:
    """
    Message:
        Returns all tasks with status is_complete = False
    Returns:
      Task: all tasks with status is_complete = False
    """
    return Task.objects.filter(is_complete=False)


class RegisterUser(CreateAPIView):
    """
    Add the user into system
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

    def perform_create(self, serializer) -> None:
        """
        Message: Saving user into system with valid password hashing
        Parameters:
            serializer (serializer): Serializer containing valid data
        Returns:
            None
        """
        user = serializer.save()
        user.set_password(serializer.data['password'])
        user.save()


class TaskListCreateView(ListCreateAPIView):
    """
    Create and Show list of tasks
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self) -> Task:
        """
        Message: Filtering tasks queryset according to login user.
        Parameters:
            self:
        Returns:
            tasks (queryset): Queryset of all tasks related to current user
        """

        token = self.request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user = valid_data['user_id']
        print('this is current user:\n' + str(user))
        print('request from ' + str(self.request.user))
        tasks = get_tasks().filter(owner=user)
        self.queryset = tasks
        return tasks

    def create(self, request, *args, **kwargs) -> Response:
        """
        Message: Create new task
        Parameters:
            self:
            request: Request from user for task creation
        Returns:
            Response:
        """

        token = self.request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user = valid_data['user_id']

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(pk=user)
        serializer.validated_data['owner'] = user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    Get, Update and Delete specific task
    """

    def get_queryset(self) -> Task:
        """
        Message: Filtering queryset according to current login user.
        Parameters:
            self:
        Returns:
            Task (queryset): Queryset of all tasks related to current user
        """

        token = self.request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]

        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user = valid_data['user_id']
        tasks = get_tasks().filter(owner=user, is_complete=False)
        self.queryset = tasks
        return tasks

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TaskSerializer
    renderer_classes = [JSONRenderer]


class SoftDeleteTask(DestroyAPIView):
    """ Task will be deleted but available in database. """

    authentication_classes = [JWTAuthentication]
    queryset = get_tasks()

    def perform_destroy(self, instance) -> None:
        """
        Message: Set is_complete status to True.
        Parameters:
             self:
             instance: task to be soft deleted
        Returns:
            None
        """
        instance.is_complete = True
        instance.completed_date = datetime.datetime.now()
        instance.save()


class ShowUserProfile(ListAPIView):
    """
    Show information of currently Login user
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Message: Filtering queryset according to current login user.
        Parameters:
            self:
        Returns:
            Task (queryset): Queryset of all tasks related to current user
        """

        token = self.request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user = valid_data['user_id']
        user = User.objects.get(pk=user)
        return [user]


class Temp(ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        data = Task.objects.all()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)
