from faker import Faker
from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    def setUp(self) -> None:
        self.login_url = reverse('customuser-login')
        self.register_url = reverse('customuser-register')

        self.id = 999
        self.list_url = reverse('artist-list')
        self.detail_url = reverse('artist-detail', args=[f'{self.id}'])

        self.fav_id = 999
        self.favorite_list_url = reverse('artists-userfavorite-list')
        self.favorite_detail_url = reverse('artists-userfavorite-detail', args=[f'{self.fav_id}'])
        self.faker = Faker()

        self.artist_data = {
            'nickname': self.faker.pystr(max_chars=10),
            'first_name': self.faker.pystr(max_chars=10),
            'last_name': self.faker.pystr(max_chars=10),
            'date_of_birth': self.faker.date_object(),
            'photo': self.faker.pystr(max_chars=10),
            'about': self.faker.pystr(max_chars=10),

        }

        self.user_data = {
            'email': self.faker.email(),
            'username': self.faker.simple_profile()['username'],
            'password': self.faker.password(length=8),
        }

        return super().setUp()

    def change_id(self, id):
        self.id = id
        self.detail_url = reverse('artist-detail', args=[f'{self.id}'])

    def change_fav_id(self, id):
        self.fav_id = id
        self.favorite_detail_url = reverse('artists-userfavorite-detail', args=[f'{self.fav_id}'])

    def tearDown(self) -> None:
        return super().tearDown()
