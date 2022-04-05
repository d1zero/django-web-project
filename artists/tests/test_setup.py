from django.test import TestCase
from faker import Faker


class ArtistTestSetUp(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.artist_data = {
            'nickname': cls.faker.simple_profile()['username'],
            'first_name': cls.faker.simple_profile()['name'],
            'last_name': cls.faker.simple_profile()['name'],
            'date_of_birth': cls.faker.simple_profile()['birthdate'],
            'photo': cls.faker.pystr(max_chars=10),
            'about': cls.faker.pystr(max_chars=10),
        }
