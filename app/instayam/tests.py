from django.test import TestCase, Client
from django.urls import reverse
import pytest
from django.forms import DateField
from Posts.models import Posts
from YamUsers.models import YamUser


class PostTestCase(TestCase):
    def setUp(self):
        user1 = YamUser.objects.create(
            username="Snake", password="weinerdog", country="USA")
        Posts.objects.create(username=user1, post_text="Hi there!")

    def test_create_post(self):
        user1 = YamUser.objects.get(username='Snake')
        self.assertEqual("Hi there!", Posts.objects.get(
            username=user1).post_text)


class YamUserTestCase(TestCase):
    def setUp(self):
        YamUser.objects.create(username="Banana_Man",
                               password="solidsnake", country="USA")

    def test_create(self):
        self.assertEqual("USA", YamUser.objects.get(
            username="Banana_Man").country)

    def test_api_login(self):
        client = Client()
        response = client.post(
            '/login/', {'username': 'Banana_Man'}, format='json')
        self.assertEqual(200, response.status_code)


@pytest.mark.django_db
def test_create_user():
    user = YamUser.objects.create(
        username='JohnSmith123',
        password='Xbox360PS5FoLife'
    )
    assert user.username == "JohnSmith123"


def test_create_post():
    content = Posts.objects.create(
        content='Wow this picture is great',
        created_at='June 29th, 1985',
        user_id=1
    )
    assert content.content == "Wow this picture is great"
