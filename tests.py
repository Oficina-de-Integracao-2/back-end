from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from professor.models import Professor
from professor.serializers import ProfessorSerializer


class ProfessorSerializerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Professor.objects.create_user(
            username='testuser',
            email='<EMAIL>',
            password='password',
            first_name='Test',
            last_name='User',
            cpf='12345678901',
        )
        self.serializer = ProfessorSerializer(self.user)

    def test_create(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': '<EMAIL>',
            'username': 'johndoe',
            'cpf': '12345678901',
            'password': 'password',
        }
        response = self.client.post(
            '/api/professors/',
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = Professor.objects.get(username=data['username'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.cpf, data['cpf'])

    def test_update(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': '<EMAIL>',
            'username': 'janedoe',
            'cpf': '12345678901',
            'password': 'password',
        }
        response = self.client.put(
            f'/api/professors/{self.user.id}/',
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = Professor.objects.get(id=self.user.id)
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.cpf, data['cpf'])

    def test_validate_cpf(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': '<EMAIL>',
            'username': 'johndoe',
            'cpf': '1234567890',
            'password': 'password',
        }
        serializer = ProfessorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['cpf'][0], 'CPF must contain exactly 11 numeric digits.')

    def test_fields(self):
        fields = [
            'id',
            'first_name',
            'last_name',
            'is_superuser',
            'email',
            'username',
            'cpf',
            'password',
        ]
        self.assertEqual(self.serializer.fields.keys(), fields)