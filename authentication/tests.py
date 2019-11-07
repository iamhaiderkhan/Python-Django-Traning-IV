from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
import json
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from .serializers import UserSerializer, UserSerializerWithJWT, UserRetrieveUpdateDestroySerializer
# Create your tests here.
client = Client()
JSON ='application/json'


class CreateNewUserTest(TestCase):
    def setUp(self):

        self.valid_signup_payload = {'email': 'haiderkhan.live@gmail.com',
            'username': "iamhaiderkhan",
            'password': '4k84u5gfju'
        }

        self.invalid_signup_payload = {
            'email': 'haiderkhan.live@gmail.com',
            'username': '',
            'password': '4k84u5gfju'
        }

    def test_create_valid_user(self):
        response = client.post(
            reverse('signup'),
            data=json.dumps(self.valid_signup_payload),
            content_type=JSON
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):

        response = client.post(
            reverse('signup'),
            data=json.dumps(self.invalid_signup_payload),
            content_type=JSON
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AllUserListTest(TestCase):


    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@test.com', password='test_@/.^')
        self.payload = api_settings.JWT_PAYLOAD_HANDLER(self.user)
        self.token = api_settings.JWT_ENCODE_HANDLER(self.payload)
        self.headers = {'HTTP_AUTHORIZATION': 'JWT ' + self.token}


    def test_get_all_user(self):

        response = client.get(reverse('users-list'), **self.headers)
        users = User.objects.all()
        serialize = UserSerializer(users, many=True)
        self.assertEqual(response.data, serialize.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetUpdateDeleteUserTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', email='test@test.com', password='test_@/.^')
        self.payload = api_settings.JWT_PAYLOAD_HANDLER(self.user)
        self.token = api_settings.JWT_ENCODE_HANDLER(self.payload)
        self.headers = {'HTTP_AUTHORIZATION': 'JWT ' + self.token}
        self.valid_payload = {
            'username': 'test_user_update',
            'email': 'test7@test.com',

        }
        self.invalid_payload = {
            'username': 'test_user_update',
            'email': 'test@test.com',
        }

        self.user1 = User.objects.create_user(username='test_user1', email='test1@test.com', password='test_@/.^')
        self.user2 = User.objects.create_user(username='test_user2', email='test2@test.com', password='test_@/.^')
        self.user3 = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_@/.^')

    def test_get_valid_single_user(self):
        response = client.get(reverse('user-get-update-delete', kwargs={'pk': self.user1.pk}), **self.headers)
        serialize = UserRetrieveUpdateDestroySerializer(self.user1)
        self.assertEqual(response.data, serialize.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_user(self):
        response = client.get(reverse('user-get-update-delete', kwargs={'pk': 51}), **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_user(self):
        response = client.put(
            reverse('user-get-update-delete', kwargs={'pk': self.user2.pk}),
            data=json.dumps(self.valid_payload),
            content_type=JSON,
            **self.headers)
        self.assertEqual(self.valid_payload['username'], response.data['username'])
        self.assertEqual(self.valid_payload['email'], response.data['email'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_user(self):
        response = client.put(
            reverse('user-get-update-delete', kwargs={'pk': self.user2.pk}),
            data = json.dumps(self.invalid_payload),
            content_type=JSON,
            **self.headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_valid_user(self):
        response = client.delete(
            reverse('user-get-update-delete', kwargs={'pk': self.user3.pk}),
            **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_user(self):
        response = client.delete(
            reverse('user-get-update-delete', kwargs={'pk': 81}),
            **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)