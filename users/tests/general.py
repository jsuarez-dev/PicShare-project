# Platzigram test
# Django
from django.test import TestCase, Client
# Models
from users.models import Profile, User


class UserModeTestCase(TestCase):
    """User model test"""
    def setUp(self):
        """Creating user and profile"""
        user = User.objects.create(
            username='jadry92',
            email='jadry@google.com',
            password='123456',
            phone_number=123456789
        )

        Profile.objects.create(
            user=user,
            phone_number=user.phone_number,
            website='www.jadry92.com',
            biography='dsahjkghfkjhsdafkjhasdjkfhklasdh'
        )

    def test_user_and_profile_are_created(self):
        """Check if user and profile has ben created properly"""
        user = User.objects.get(username='jadry92')
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(user)
        self.assertIsNotNone(Profile)
        self.assertEqual(profile.website, 'www.jadry92.com')
        self.assertEqual(user.password, '123456')

    def test_create_an_user(self):
        """Create an new user"""
        c = Client()
        response = c.post('/users/signup/', {
            'username': 'john123',
            'password': '12345',
            'password_confirmation': '12345',
            'first_name': 'john',
            'last_name': 'smith',
            'email': 'john@smith.io'
        })
        print(response.context)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """Login test"""
        c = Client()
        response = c.post('/users/login/', {'username': 'jadry92', 'password': '123456'})
        self.assertEqual(response.status_code, 200)