from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from users.models import User, Profile


class TestViews(TestCase):

    def test_should_show_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_should_show_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_should_signup_user(self):
        self.user = {
            "username": "username",
            "email": "email@gmail.com",
            "address": "address",
            "phone_number": "9228110548",
            "password1": "password",
            "password2": "password"
        }
        response = self.client.post(reverse('register'), self.user)
        self.assertEquals(response.status_code, 302)

    def test_should_not_signup_user_with_taken_name(self):
        self.user = {
            "username": "user1",
            "email": "inexture1@gmail.com",
            "address": "address",
            "phone_number": "9228110549",
            "password1": "pass@123",
            "password2": "pass@123"
        }

        self.client.post(reverse('register'), self.user)
        response = self.client.post(reverse('register'), self.user)
        self.assertEqual(response.status_code, 302)

        storage = list(get_messages(response.wsgi_request))
        # print("Username Is Already Taken")
        # print(storage)
        # for i in storage:
        #     print("hi")
        #     print(i)
        self.assertIn("Username Is Already Taken",
                      list(map(lambda x: x.message, storage)))

    def test_should_not_signup_user_with_taken_email(self):
        self.user = {
            "username": "user1",
            "email": "inexture1@gmail.com",
            "address": "address",
            "phone_number": "9228110549",
            "password1": "pass@123",
            "password2": "pass@123"
        }
        self.test_user = {
            "username": "user2",
            "email": "inexture1@gmail.com",
            "address": "address",
            "phone_number": "9228110549",
            "password1": "pass@123",
            "password2": "pass@123"
        }

        self.client.post(reverse('register'), self.user)
        response = self.client.post(reverse('register'), self.test_user)
        self.assertEqual(response.status_code, 302)

        storage = list(get_messages(response.wsgi_request))
        # print("Username Is Already Taken")
        # print(storage)
        # for i in storage:
        #     print("hi")
        #     print(i)
        self.assertIn("Email Is Already Taken",
                      list(map(lambda x: x.message, storage)))

    def test_should_login_successfully(self):
        user = User.objects.create_user(username="user1",email="shahil1@gmail.com",address="address",phone_number="9228110541",password="pass@123")
        response = self.client.post(reverse('login'), {
            'email': user.email,
            'password': 'pass@123'
        })
        self.assertEquals(response.status_code, 302)

        storage = get_messages(response.wsgi_request)

        self.assertIn("You are now logged in!!",
                      list(map(lambda x: x.message, storage)))

    def test_should_not_login_with_invalid_password(self):
        user = User.objects.create_user(username="user1",email="inexture1@gmail.com",address="address",phone_number="9228110549",password="pass@123")
        response = self.client.post(reverse('login'), {
            'email': user.email,
            'password': 'pass@1234'
        })
        self.assertEquals(response.status_code, 302)

        storage = get_messages(response.wsgi_request)

        self.assertIn("Invalid Credentials",
                      list(map(lambda x: x.message, storage)))

    def test_should_show_profile_page(self):
        user = User.objects.create_user(username="user1", email="inexture1@gmail.com", address="address",
                                        phone_number="9228110549", password="pass@123")
        self.client.post(reverse('login'), {
            'email': user.email,
            'password': 'pass@123'
        })
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_should_update_profile(self):
        user = User.objects.create_user(username="user1", email="inexture1@gmail.com", address="address",
                                        phone_number="9228110549", password="pass@123")
        self.client.post(reverse('login'), {
            'email': user.email,
            'password': 'pass@123'
        })
        response = self.client.post(reverse('profile'), {
            'username':'inx',
            'email': 'inx@gmail.com',

        })

        self.assertEquals(response.status_code, 302)

        storage = get_messages(response.wsgi_request)

        self.assertIn(f'Your account has been updated!',
                              list(map(lambda x: x.message, storage)))

    def test_should_show_change_password_page(self):
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_change.html')

    def test_should_change_password(self):
        user = User.objects.create_user(username="user1", email="inexture1@gmail.com", address="address",
                                        phone_number="9228110549", password="pass@123")
        self.client.post(reverse('login'), {
            'email': user.email,
            'password': 'pass@123'
        })
        response = self.client.post(reverse('change_password'), {
            'old_password': 'pass@123',
            'new_password1': 'pass@1234',
            'new_password2': 'pass@1234'

        })

        self.assertEquals(response.status_code, 302)

        storage = get_messages(response.wsgi_request)

        self.assertIn('Your password was successfully updated!',
                              list(map(lambda x: x.message, storage)))

    def test_should_not_change_password(self):
        user = User.objects.create_user(username="user1", email="inexture1@gmail.com", address="address",
                                        phone_number="9228110549", password="pass@123")
        self.client.post(reverse('login'), {
            'email': user.email,
            'password': 'pass@123'
        })
        response = self.client.post(reverse('change_password'), {
            'old_password': 'pass@123',
            'new_password1': 'pass@123',
            'new_password2': 'pass@1234'

        })

        self.assertEquals(response.status_code, 200)

        storage = get_messages(response.wsgi_request)

        self.assertIn('Please correct the error below.',
                              list(map(lambda x: x.message, storage)))