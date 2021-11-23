"""
This module contains Apis
"""

from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.backends import TokenBackend
from .serializers import UserSerializer, TaskSerializer
from .models import Task


def hello(request) -> HttpResponse:
    """
    Show Main Page
    """
    return HttpResponse(f'<h1>hello {request.META.get("PATH")}</h1>')


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

#
# class UserLoginView(RetrieveAPIView):
#
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = UserLoginSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         response = {
#             'success': 'True',
#             'status code' : status.HTTP_200_OK,
#             'message': 'User logged in  successfully',
#             'token': serializer.data['token'],
#             }
#         status_code = status.HTTP_200_OK
#
#         return Response(response, status=status_code)


class TaskListCreateView(ListCreateAPIView):
    """
    Create and Show list of tasks
    """
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
        tasks = Task.objects.filter(owner=user)
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
    serializer_class = TaskSerializer
    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


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
        tasks = Task.objects.filter(owner=user)
        self.queryset = tasks
        return tasks

    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TaskSerializer
    renderer_classes = [JSONRenderer]
