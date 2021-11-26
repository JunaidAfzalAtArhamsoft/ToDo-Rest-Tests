"""
This module test to_do_api app's all apis
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Task


class GenericTest(APITestCase):
    """
    Provide basic setup for test cases.
    """

    def setUp(self) -> None:
        """
        As most testcases required user and JWT token.
        It provide this basic setup.
        """
        self.user = User.objects.create_user(
            first_name='test',
            last_name='test',
            username='test',
            email='test@test.com',
            password='test'

        )
        url = reverse('token_obtain_pair')
        response = self.client.post(
            path=url,
            data={'username': 'test', 'password': 'test'},
            format='json'
        )
        self.token = response.data['access']
        self.headers = {
            'accept': 'application/json',
            'HTTP_AUTHORIZATION': f'Bearer {self.token}',
        }
        self.client.login(username='test', password='12345678qQ')

    def create_task(self, title='test', is_complete='False') -> Task:
        """
        Create task for testing
        Parameters:
            self:
            title: Task title
            is_complete: Is task soft deleted or not.
        Returns:
            task: Task object
        """
        self.task = Task(  # pylint: disable=W0201
            task_title=title,
            task_description="test delete description",
            is_complete=is_complete,
            task_category="Home_task",
            start_date="2021-11-19T12:13:10.149Z",
            completed_date="2021-11-19T12:13:10.149Z",
            owner=self.user
        )
        self.task.save()
        return self.task

    @staticmethod
    def get_tasks(key):
        """
        Return list of tasks
        """
        return Task.objects.get(pk=key)  # pylint: disable=E1101


class RegistrationTestCase(APITestCase):
    """
    Test User Registration In different cases.
    """

    def test_registration_valid_data(self) -> None:
        """
        Testing User Registration with valid data
        """
        data = {
            'username': 'test_user',
            'email': 'test_user@test.com',
            'password': 'Test_user_password_123',

        }

        url = '/register/'
        response1 = self.client.post(url, data)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

    def test_registration_already_exist(self) -> None:
        """
        Testing User Registration with already registered username
        """

        data = {
            'username': 'test_user1',
            'email': 'test_user1@test.com',
            'password': '123',

        }
        url = '/register/'
        self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_data(self) -> None:
        """
        Testing User Registration with missing password
        """

        data = {
            'username': 'test_user',
            'email': 'test_user1@test.com',
        }
        url = '/register/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserTestCase(GenericTest):
    """
    Test login api with valid and invalid credentials.
    """

    def test_valid_login_user(self) -> None:
        """
        testing login api with valid credentials
        """

        url = '/login/'
        data = {
            'username': 'test',
            'password': 'test'
        }
        response = self.client.post(
            path=url,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login_username(self) -> None:
        """
        testing login api with correct username and incorrect password
        """

        data = {
            'username': 'tes',
            'password': 'test'
        }
        url = '/login/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_login_user_password(self) -> None:
        """
        testing login api with incorrect username and correct password
        """

        data = {
            'username': 'test',
            'password': 'tesT'
        }
        url = '/login/'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordTestCase(GenericTest):
    """
    Test Forgot Password api
    """

    def setUp(self) -> None:
        """
        Setting User and url of api
        """
        super().setUp()
        self.url = '/api/password_reset/'

    def test_forgot_password_registered_user(self) -> None:
        """
        Testing api with registered email
        """

        data = {
            "email": "test@test.com"
        }

        response = self.client.post(
            path=self.url,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forgot_password_unregistered_user(self) -> None:
        """
        Testing forgot password for invalid email.
        """
        data = {
            "email": "invalid_email@test.com'"
        }
        response = self.client.post(
            path=self.url,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteTaskTestCase(GenericTest):
    """
    Delete Task api Test
    """

    def setUp(self) -> None:
        """
        Setup required things for task get i.e user.
        """
        super().setUp()
        self.task1 = self.create_task()
        self.task2 = self.create_task()
        self.task3 = self.create_task()

    def test_soft_delete_task_valid(self):
        """
        Testing authorized soft delete api that delete task
        but available in database and hidden from user
        """

        url = f'/tasks/soft-delete/{self.task.pk}/'
        response = self.client.delete(
            path=url,
            **self.headers
        )

        my_task = Task.objects.get(pk=self.task.pk)  # pylint: disable=E1101
        self.assertEqual(my_task.is_complete, True)

        number_tasks_in_db = len(Task.objects.all())  # pylint: disable=E1101
        self.assertEqual(number_tasks_in_db, 3)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_soft_delete_task_already_deleted(self):
        """
        Testing authorized soft delete api that delete the task
        that already soft deleted.
        """

        url = f'/tasks/soft-delete/{self.task3.pk}/'
        self.client.delete(
            path=url,
            **self.headers
        )
        response = self.client.delete(
            path=url,
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_soft_delete_task_invalid(self):
        """
        Testing unauthorized soft delete api that delete task
        but available in database and hidden from user
        """
        url = f'/tasks/soft-delete/{self.task.pk}/'
        response = self.client.delete(
            path=url,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_task(self):
        """
        Testing Delete api that permanently delete task
        """
        url = f'/tasks/{self.task.pk}/'
        response = self.client.delete(
            path=url,
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # There must be 2 tasks available in db now
        number_tasks_in_db = len(Task.objects.all())  # pylint: disable=E1101
        self.assertEqual(number_tasks_in_db, 2)


class ViewTaskTestCase(GenericTest):
    """
    Test View task on different conditions.
    """

    def setUp(self) -> None:
        """
        Setup required things for task creating i.e user.
        """
        super().setUp()
        self.task = self.create_task(title='test view task1')
        self.task1 = self.create_task(title='test view task2')

    def test_valid_task_view(self):
        """
        Test for viewing all tasks of same user.
        Getting tasks with JWT
        """

        response = self.client.get(
            path='/tasks/',
            **self.headers
        )
        # Getting task result from response
        result_from_response = response.data['results']

        # There must be 2 task in result as we add 2 task for test user.
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Task ordering must be based on task ID otherwise it may fail.
        self.assertEqual(result_from_response[0]['task_title'], 'test view task1')
        self.assertEqual(result_from_response[1]['task_title'], 'test view task2')

    def test_invalid_task_view(self):
        """
        Test for viewing all tasks of user.
        Getting tasks without JWT
        """

        response = self.client.get(
            path='/tasks/',
        )
        # Status will be 401 as we do not provide JWT token.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateTaskTestCase(GenericTest):
    """
    Test Task Creation
    """

    def setUp(self) -> None:
        """
        Setup required things for task creating i.e user.
        """

        super().setUp()
        self.url = '/tasks/'

    def test_valid_create_task(self) -> None:
        """
        Testing create task api with valid data
        """

        data = {
            "task_title": "test_task",
            "task_description": "test_description",
            "is_complete": False,
            "task_category": "Home_task",
            "start_date": "2021-11-19T12:13:10.149Z",
            "completed_date": "2021-11-19T12:13:10.149Z",
        }

        response = self.client.post(
            path=self.url,
            data=data,
            **self.headers
        )
        tasks = Task.objects.all()  # pylint: disable=E1101
        self.assertEqual(len(tasks), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_task(self) -> None:
        """
        Testing create task api with invalid data
        """

        # missing category
        data = {
            "task_title": "test_task",
            "task_description": "test_description",
            "is_complete": False,
            "start_date": "2021-11-19T12:13:10.149Z",
            "completed_date": "2021-11-19T12:13:10.149Z",
        }
        response = self.client.post(
            path=self.url,
            data=data,
            **self.headers
        )
        tasks = Task.objects.all()  # pylint: disable=E1101
        self.assertEqual(len(tasks), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetTaskTestCase(GenericTest):
    """
    Testing Get api
    """

    def setUp(self) -> None:
        """
        Setup required things for task get i.e user.
        """
        super().setUp()

        self.task = self.create_task(title="test get task")
        self.task = self.create_task(title="test get task1")

    def test_get_task(self) -> None:
        """
        Testing get all tasks api
        """

        url = '/tasks/'
        response = self.client.get(
            path=url,
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_task(self) -> None:
        """
        Testing get specific task api
        """

        url = f'/tasks/{self.task.pk}/'
        response = self.client.get(path=url, **self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_specific_task(self):
        """
        Testing get specific task api
        """

        url = f'/tasks/{0}/'
        response = self.client.get(path=url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateTaskTestCase(GenericTest):
    """
    Testing put patch apis
    """

    def setUp(self) -> None:
        """
        Setup required things for task get i.e user and creating tasks.
        """

        super().setUp()

        self.task = self.create_task(title='get task')
        self.task1 = self.create_task(title='get task 1')

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
        response = self.client.put(
            path=url,
            data=data,
            **self.headers
        )
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

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.status_code, status.HTTP_200_OK)


class ShowUserTestCase(GenericTest):
    """
    Test User profile show api
    """

    def test_show_valid_user_profile(self):
        """
        Testing show_user_profile api with JWT
        """

        url = '/profile/'
        response = self.client.get(
            path=url,
            **self.headers
        )

        user_profile = response.data['results']
        user_profile = user_profile[0]
        username = user_profile['username']
        email = user_profile['email']

        self.assertEqual(username, 'test')
        self.assertEqual(email, 'test@test.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_invalid_user_profile(self):
        """
        Testing show_user_profile api without JWT
        """

        url = '/profile/'
        response = self.client.get(
            path=url,
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
