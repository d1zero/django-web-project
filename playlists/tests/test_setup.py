from django.test import TestCase
from faker import Faker


class PlaylistTestSetUp(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.playlist_data = {
            'name': cls.faker.pystr(max_chars=10),
            'description': cls.faker.pystr(max_chars=10),
            'photo': cls.faker.pystr(max_chars=10),
            'is_visible': cls.faker.pybool(),
        }

