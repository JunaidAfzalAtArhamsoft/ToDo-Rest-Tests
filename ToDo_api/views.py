from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenBackendError
from .serializers import UserSerializer, TaskSerializer
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import status
from django.http import Http404
from .models import Task


def hello(request):
    """
    Show Main Page
    """
    return HttpResponse('<h1>hello</h1>')


class RegisterUser(CreateAPIView):
    """
    Add the user into system
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]

    def perform_create(self, serializer):
        """
        Message: Saving user into system
        Parameters:
            serializer (serializer): Serializer containing valid data
        Returns:
            None
        """
        user = serializer.save()
        user.set_password(serializer.data['password'])
        user.save()
#
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
    def get_queryset(self):
        """
        Message: Filtering tasks queryset according to login user.
        Parameters:
            self:
        Returns:
            tasks (queryset): Queryset of all tasks related to current user
        """
        # owner = self.request.user
        # owner = User.objects.filter(username=owner)
        token = self.request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user = valid_data['user_id']
            print('this is current user:\n' + str(user))
            tasks = Task.objects.filter(owner=user)
            self.queryset = tasks
            return tasks
        except TokenBackendError:
            raise Http404('Token Expired')

    def create(self, request, *args, **kwargs):
        """
        Message: Create new task
        Parameters:
            self:
            request: Request from user for task creation
        Returns:
            Response:
        """
        token = self.request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user = valid_data['user_id']

            serializer = self.get_serializer(data=request.data)
            # owner = User.objects.filter(username=self.request.user)
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(pk=user)
            serializer.validated_data['owner'] = user
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except TokenBackendError:
            raise Http404('Token Expired')

    # queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    # renderer_classes = [JSONRenderer]
    # lookup_url_kwarg = {'url': 'ToDo_REST:tasks-detail'}


class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    Get, Update and Delete specific task
    """

    def get_queryset(self):
        """
        Message: Filtering queryset according to current login user.
        Parameters:
            self:
        Returns:
            tasks (queryset): Queryset of all tasks related to current user
        """
        # owner = self.request.user
        # owner = User.objects.filter(username=owner)
        token = self.request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        try:
            valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
            user = valid_data['user_id']
            tasks = Task.objects.filter(owner=user)
            self.queryset = tasks
            return tasks
        except TokenBackendError:
            raise Http404('Token Expired')

    # permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TaskSerializer
    renderer_classes = [JSONRenderer]


# class LoginApiView(GenericAPIView):
#     serializer_class = UserLoginSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#


# def send(token):
#     token = str(uuid.uuid4())
#     subject = 'Reset Password'
#     message = f'Hi. I am Kabu from TaskManagementSystem.\n You can reset your password from below ' \
#               f'link.\nhttp:\\127.0.0.1:8000/forgot-password/{token}/ '
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = ['NoumanAkram.Arhamsoft@gmail.com', 'junaidafzal.arhamsoft@gmail.com']
#     send_mail(subject=subject, message=message, from_email=email_from,
#     recipient_list=['junaidafzal.arhamsoft@gmail.com'])
#     return redirect()
