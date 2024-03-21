from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {'first_name': 'Mer', 'last_name': 'M', 'username': 'mermer1',
                     'email': 'r@gmail.com', 'password1': '12345678_M', 'password2': '12345678_M'}

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):
        # проверяем что пользователя не существует до отправки формы
        self.assertFalse(User.objects.filter(username=self.data['username']).exists())

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # self.assertRedirects(response, reverse('users:index'))

        # проверим что пользователь создан
        self.assertTrue(User.objects.filter(username=self.data['username']).exists())

        # проверим создание объекта для отправки письма
        email_verification = EmailVerification.objects.filter(user__username=self.data['username'])
        self.assertTrue(email_verification.exists())

    def test_user_registration_post_error(self):
        # user = User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertContains(response, 'Пользователь с таким именем уже существует')
