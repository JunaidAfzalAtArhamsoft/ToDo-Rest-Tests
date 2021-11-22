from django.contrib.auth.models import User, update_last_login
from rest_framework import serializers
from .models import Task


class UserSerializer(serializers.ModelSerializer):
    """
    Serialize User Model
    """
    password = serializers.CharField(
        style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class TaskSerializer(serializers.ModelSerializer):
    """
    Serialize Task Model
    """
    link = serializers.SerializerMethodField()

    class Meta:
        model = Task

        fields = ['task_title', 'task_description', 'is_complete', 'task_category',
                  'start_date', 'completed_date', 'owner', 'link']
        read_only_fields = ('owner',)

    def get_link(self, obj):
        """
        Message: Create reference for every task to view specifically.
        Parameters:
            self:
            obj (Task): Task object
        Returns:
            Address of Task
        """
        return 'http://127.0.0.1:8000/tasks/{}'.format(obj.id)

#
# class LogInSerializer(serializers.Serializer):
#     """
#     Serialize email and password of user and and validate it.
#     """
#     email = serializers.EmailField()
#     password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'})
#
#     def validate(self, attrs):
#         """
#
#         """
#         email = attrs.get('email', '')
#         password = attrs.get('password', '')
#         user = authenticate(email=email, password=password)
#
#         if not user:
#             raise AuthenticationFailed('Invalid Credentials.')
#         if not user.is_Ative:
#             raise AuthenticationFailed('Account disabled or not exist.')
#
#         return {
#             'email': email,
#             'username': user.username,
#             'tokens': user.token()
#         }
#         # return super().validate(attrs)
#
#


# JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
# JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
#
#
# class UserLoginSerializer(serializers.Serializer):
#
#     email = serializers.CharField(max_length=255)
#     password = serializers.CharField(max_length=128)
#     token = serializers.CharField(max_length=255, read_only=True)
#
#     def validate(self, data):
#         email = data.get("email", None)
#         password = data.get("password", None)
#         user = User.objects.filter(email=email)
#
#         if len(user) == 0:
#             raise serializers.ValidationError(
#                 'A user with this email and password is not found.'
#             )
#         try:
#             user = user[0]
#             url = 'http://127.0.0.1:8000/login/'
#             resp = requests.post(url, {'username': 'noman', 'password': '12345678qQ'})
#             print(resp)
#
#         except User.DoesNotExist:
#             raise serializers.ValidationError(
#                 'User with given email and password does not exists'
#             )
#         return {
#             'email': user.email,
#             # 'token': resp.
#         }
