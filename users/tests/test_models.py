from django.test import TestCase
from users.models import User,Profile


class TestUser(TestCase):
    def test_should_create_user(self):
        user = User.objects.create(username="user12", email="shahil12@gmail.com", address="address",
                                        phone_number="9228110541", password="pass@123")
        Profile.objects.get_or_create(user=user)
        profile = Profile.objects.get(user=user)
        self.assertEqual(str(user), user.email)
        self.assertEqual(str(profile), f'{user.email} Profile')

