""" Unit-test posts"""
# Django
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
# models
from aigram.users.models import User, Profile
from aigram.posts.models import Post


class NewPostFormTest(TestCase):
    """Test of new post form class"""

    def setUp(self):
        """Creating user and profile"""
        self.client = Client()
        response = self.client.post(reverse('users:signup'), {
            'username': 'john123',
            'password': '12345',
            'password_confirmation': '12345',
            'birthday': '10/10/1990',
            'first_name': 'john',
            'last_name': 'smith',
            'email': 'john@smith.io'
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('users:email_confirm_sent'))
        self.assertEquals(User.objects.get(username='john123').email, 'john@smith.io')

        user = User.objects.get(username='john123')
        user.is_verified = True
        user.save()

        self.mock_photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=open(
                'functional_test/fixtures/img/profile/img_test.001.png',
                'rb'
                ).read(),
            content_type='image/png')

        profile = Profile.objects.get(user__username='john123')
        profile.website = 'www.john123.com',
        profile.biography = 'dsahjkghfkjhsdafkjhasdjkfhklasdh'
        profile.picture = self.mock_photo
        profile.gender = 'R'
        profile.save()

    def test_form_normal(self):
        """usual test case"""
        # login
        response = self.client.login(
            username='john123',
            password='12345'
        )

        self.assertTrue(response)

        file_mock = open('functional_test/fixtures/img/profile/img_test.001.png', 'rb')
        caption = 'My first photo #first @someone'
        request = self.client.post(reverse('posts:create'), {
            'caption': caption,
            'photo': file_mock,
            'location': 'melbourne'
        })

        self.assertEqual(request.status_code, 302)
        self.assertTrue(Post.objects.filter(user__username='john123', caption=caption).exists())