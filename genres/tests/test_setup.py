from django.test import TestCase
from faker import Faker

class GenreTestSetUp(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.genre_data = {
            'name': cls.faker.pystr(max_chars=10),
            'description': cls.faker.pystr(max_chars=10),
            'cover': cls.faker.pystr(max_chars=10),
        }