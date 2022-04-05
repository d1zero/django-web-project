from django.test import TestCase
from faker import Faker


class TrackTestSetUp(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.track_data = {
            'title':cls.faker.pystr(max_chars=10),
            'date_of_release': cls.faker.date_object(),
            'soundtrack': cls.faker.pystr(max_chars=10),
            'cover': cls.faker.pystr(max_chars=10),
            'description': cls.faker.pystr(max_chars=10),
        }
