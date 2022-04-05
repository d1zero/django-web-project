from django.test import TestCase
from faker import Faker
from random import choice


class AlbumTestSetUp(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.album_data = {
            'name': cls.faker.pystr(max_chars=10),
            'date_of_release': cls.faker.date_object(),
            'description': cls.faker.pystr(max_chars=10),
            'cover': cls.faker.pystr(max_chars=10),
            'type_of_album': choice(['Сингл', 'EP', 'Альбом']),
        }
