from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import UserSerializer
from django.urls import reverse


class RegistrationTestCase(APITestCase):
    """
    Test User Registration In different cases.
    """

    def test_registration(self):
        data = {
            'username': 'test_user',
            'email': 'test_user@test.com',
            'password': 'Test_user_password_123',

        }
        data1 = {
            'username': 'test_user',
            'email': 'test_user1@test.com',
            'password': '123',

        }
        # url = reverse('/ToDo/register/')
        url = '/register/'
        response1 = self.client.post(url, data)
        response2 = self.client.post(url, data)
        response3 = self.client.post(url, data1)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserTestCase(APITestCase):
    """
    Test login api with valid and invalid credentials.
    """

    def setUp(self) -> None:
        user = User.objects.create_user(
            first_name='test',
            last_name='test',
            email='test@test.com',
            username='test',
            password='test'
        )

    def test_login_user(self):
        url = '/login/'
        data1 = {
            'username': 'test',
            'password': 'test'
        }
        data2 = {
            'username': 'test',
            'password': 'tes'
        }
        data3 = {
            'username': 'testT',
            'password': 'tesT'
        }
        response1 = self.client.post(url, data1)
        response2 = self.client.post(url, data2)
        response3 = self.client.post(url, data3)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response3.status_code, status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordTestCase(APITestCase):
    """
    Test Forgot Password api
    """

    def test_forgot_password(self):
        user = User.objects.create_user(
            first_name='test',
            last_name='test',
            email='junaidafzal.arhamsoft@gmail.com',
            username='test',
            password='test'
        )
        url = '/api/password_reset/'
        data1 = {
            "email": "junaidafzal.arhamsoft@gmail.com"
        }
        data2 = {
            "email": "junaid@gmail.com"
        }
        response1 = self.client.post(url, data1)
        response2 = self.client.post(url, data2)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


class ViewTaskTestCase(APITestCase):
    """
    Test View task on different conditions.
    """

    def setUp(self) -> None:
        """
        Setup required things for task creating i.e user.
        """
        user = User.objects.create_user(
            first_name='test',
            last_name='test',
            email='junaidafzal.arhamsoft@gmail.com',
            username='test',
            password='test'
        )
        data1 = {
            'username': 'test',
            'password': 'test'
        }
        self.client.post('/login/', data1)



class CreateTaskTestCase(APITestCase):
    """
    Test Task Creation
    """

    def setUp(self) -> None:
        """
        Setup required things for task creating i.e user.
        """

        self.user = User.objects.create_user(
            first_name='test',
            last_name='test',
            email='junaidafzal.arhamsoft@gmail.com',
            username='test',
            password='12345678qQ'
        )
        self.user.save()

        data = {
            'username': 'test',
            'password': '12345678qQ'
        }

        response = self.client.login(username='test', password='12345678qQ')
        print(response)
        auth_client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        # self.SUPERUSER = User(auth_client.post('/v1/auth/', {'username': 'test', 'password': '12345678qQ'})
        #                       # .data['token'])

        # s = self.client.login(username='test', password='12345678qQ')
        # self.SUPERUSER = TestUser(auth_client.post('/v1/auth/', {'username': 'TestUser', 'password': 'password'})
        #                           .data['token'])
        # print(s)

    def test_create_task(self):
        refresh = RefreshToken.for_user(self.user)
        data2 = {
            "task_title": "test_task",
            "task_description": "test_description",
            "is_complete": False,
            "task_category": "Home_task",
            "start_date": "2021-11-19T12:13:10.149Z",
            "completed_date": "2021-11-19T12:13:10.149Z",
        }
        url = '/tasks/'
        response = self.client.post(url, data2)
        print(response.request.keys())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

