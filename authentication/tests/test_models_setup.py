from django.test import TestCase
from faker import Faker


class UserTestSetUp(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.user_data = {
            'email': cls.faker.email(),
            'username': cls.faker.simple_profile()['username'],
            'avatar': cls.faker.pystr(),
        }
