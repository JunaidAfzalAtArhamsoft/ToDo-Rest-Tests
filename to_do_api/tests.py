"""
This module test to_do_api app's all apis
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Task


class RegistrationTestCase(APITestCase):
    """
    Test User Registration In different cases.
    """

    def test_registration(self) -> None:
        """
        Testing User Registration
        """
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
        """
        Creating user to validating login api
        """
        User.objects.create_user(
            first_name='test',
            last_name='test',
            email='test@test.com',
            username='test',
            password='test'
        )

    def test_login_user(self) -> None:
        """
        testing login api
        """

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

    def setUp(self) -> None:
        """
        Creating User
        """
        User.objects.create_user(
            first_name='test',
            last_name='test',
            email='junaidafzal.arhamsoft@gmail.com',
            username='test',
            password='test'
        )

    def test_forgot_password(self) -> None:
        """
        Testing api with registered and unregistered email
        """

        data1 = {
            "email": "junaidafzal.arhamsoft@gmail.com"
        }
        data2 = {
            "email": "junaid@gmail.com"
        }
        url = '/api/password_reset/'
        response1 = self.client.post(path=url, data=data1)
        response2 = self.client.post(path=url, data=data2)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteTaskTestCase(APITestCase):
    """
    Delete Task api Test
    """

    def setUp(self) -> None:
        """
        Setup required things for task get i.e user.
        """
        self.user = User.objects.create_user(
            first_name='test',
            last_name='test',
            email='junaidafzal.arhamsoft@gmail.com',
            username='test',
            password='12345678qQ',
            is_staff=True
        )
        self.user.save()
        url = reverse('token_obtain_pair')
        resp = self.client.post(
            path=url,
            data={'username': 'test', 'password': '12345678qQ'},
            format='json'
        )
        self.token = resp.data['access']
        self.headers = {
            'accept': 'application/json',
            'HTTP_AUTHORIZATION': f'Bearer {self.token}',
        }

        self.client.login(username='test', password='12345678qQ')
        self.task = Task(task_title="test delete task",
                         task_description="test delete description",
                         is_complete=False,
                         task_category="Home_task",
                         start_date="2021-11-19T12:13:10.149Z",
                         completed_date="2021-11-19T12:13:10.149Z",
                         owner=self.user)
        self.task.save()

        self.task1 = Task(task_title="test soft delete task",
                          task_description="test soft delete description",
                          is_complete=False,
                          task_category="Home_task",
                          start_date="2021-11-19T12:13:10.149Z",
                          completed_date="2021-11-19T12:13:10.149Z",
                          owner=self.user)
        self.task1.save()

    def test_soft_delete_task(self):
        """
        Testing soft delete api that delete task
        but available in database and hidden from user
        """
        url = f'/tasks/soft-delete/{self.task1.pk}/'
        response = self.client.delete(path=url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task(self):
        """
        Testing Delete api that permanently delete task
        """
        url = f'/tasks/{self.task.pk}/'
        response = self.client.delete(path=url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ViewTaskTestCase(APITestCase):
    """
    Test View task on different conditions.
    """

    def setUp(self) -> None:
        """
        Setup required things for task creating i.e user.
        """
        User.objects.create_user(
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
        self.client.post(path='/login/', data=data1)


class CreateTaskTestCase(APITestCase):
    """
    Test Task Creation
    """

    def setUp(self) -> None:
        """
        Setup required things for task creating i.e user.
        """

        User.objects.create_user(
            first_name='test',
            last_name='test',
            email='junaidafzal.arhamsoft@gmail.com',
            username='test',
            password='12345678qQ',
            is_staff=True
        )
        self.client.login(username='test', password='12345678qQ')

    def test_create_task(self) -> None:
        """
        Testing create task api
        """
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username': 'test', 'password': '12345678qQ'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # self.assertTrue('token' in resp.data)
        token = resp.data['access']
        token = str(token)
        headers = {
            'accept': 'application/json',
            'HTTP_AUTHORIZATION': f'Bearer {token}',
        }
        data2 = {
            "task_title": "test_task",
            "task_description": "test_description",
            "is_complete": False,
            "task_category": "Home_task",
            "start_date": "2021-11-19T12:13:10.149Z",
            "completed_date": "2021-11-19T12:13:10.149Z",
        }
        url = '/tasks/'
        response = self.client.post(path=url, data=data2, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetTaskTestCase(APITestCase):
    """
    Testing Ge api
    """

    def setUp(self) -> None:
        """
        Setup required things for task get i.e user.
        """
        self.user = User.objects.create_user(
            first_name='test',
            last_name='test',
            email='junaidafzal.arhamsoft@gmail.com',
            username='test',
            password='12345678qQ',
            is_staff=True
        )
        self.user.save()
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username': 'test', 'password': '12345678qQ'}, format='json')
        self.token = resp.data['access']
        self.headers = {
            'accept': 'application/json',
            'HTTP_AUTHORIZATION': f'Bearer {self.token}',
        }

        self.client.login(username='test', password='12345678qQ')
        self.task = Task(task_title="test get task",
                         task_description="test get description",
                         is_complete=False,
                         task_category="Home_task",
                         start_date="2021-11-19T12:13:10.149Z",
                         completed_date="2021-11-19T12:13:10.149Z",
                         owner=self.user)
        self.task.save()

        self.task1 = Task(task_title="test get task 1",
                          task_description="test get description 1",
                          is_complete=False,
                          task_category="Home_task",
                          start_date="2021-11-19T12:13:10.149Z",
                          completed_date="2021-11-19T12:13:10.149Z",
                          owner=self.user)
        self.task1.save()

    def test_get_task(self) -> None:
        """
        Testing get all tasks api
        """
        url = '/tasks/'
        # response = self.client.login(username='test', password='12345678qQ')
        response = self.client.get(path=url, **self.headers)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_task(self) -> None:
        """
        Testing get specific task api
        """
        url = f'/tasks/{self.task.pk}/'
        response = self.client.get(path=url, **self.headers)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = f'/tasks/{0}/'
        response = self.client.get(path=url, **self.headers)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateTaskTestCase(APITestCase):
    """
    Testing put patch apis
    """

    def setUp(self) -> None:
        """
        Setup required things for task get i.e user and creating tasks.
        """
        self.user = User.objects.create_user(
            first_name='test',
            last_name='test',
            email='junaidafzal.arhamsoft@gmail.com',
            username='test',
            password='12345678qQ',
            is_staff=True
        )
        self.user.save()
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username': 'test', 'password': '12345678qQ'}, format='json')
        self.token = resp.data['access']
        self.headers = {
            'accept': 'application/json',
            'HTTP_AUTHORIZATION': f'Bearer {self.token}',
        }

        self.client.login(username='test', password='12345678qQ')
        self.task = Task(task_title="test get task",
                         task_description="test get description",
                         is_complete=False,
                         task_category="Home_task",
                         start_date="2021-11-19T12:13:10.149Z",
                         completed_date="2021-11-19T12:13:10.149Z",
                         owner=self.user)
        self.task.save()

        self.task1 = Task(task_title="test get task 1",
                          task_description="test get description 1",
                          is_complete=False,
                          task_category="Home_task",
                          start_date="2021-11-19T12:13:10.149Z",
                          completed_date="2021-11-19T12:13:10.149Z",
                          owner=self.user)
        self.task1.save()

    def test_put_task(self) -> None:
        """
        Testing Put api
        """
        url = f'/tasks/{self.task.pk}/'
        data = {
            'task_title': "test put task 1",
            'task_description': "test put description 1",
            'is_complete': False,
            'task_category': "Home_task",
            'start_date': "2022-11-19T12:13:10.149Z",
            'completed_date': "2022-11-19T12:13:10.149Z",
        }
        response = self.client.put(path=url, data=data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_task(self) -> None:
        """
        Testing patch api
        """
        url = f'/tasks/{self.task.pk}/'
        data = {
            'task_title': "test patch task 1",
            'task_description': "test patch description 1",
        }
        response = self.client.patch(path=url, data=data, **self.headers)
        result = self.client.get(path=f'/tasks/{self.task.pk}/', **self.headers)
        # print(result.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.status_code, status.HTTP_200_OK)


class ShowUserTestCase(APITestCase):
    """
    Test User profile show api
    """

    def setUp(self) -> None:
        """
        Creating User and login to test show_profile api
        """

        User.objects.create_user(
            first_name='test',
            last_name='test',
            email='junaidafzal.arhamsoft@gmail.com',
            username='test',
            password='12345678qQ',
            is_staff=True
        )
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username': 'test', 'password': '12345678qQ'}, format='json')
        self.token = resp.data['access']
        self.headers = {
            'accept': 'application/json',
            'HTTP_AUTHORIZATION': f'Bearer {self.token}',
        }

    def test_show_user_profile(self):
        """
        Testing show_user_profile api
        """

        url = '/profile/'
        response = self.client.get(path=url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
