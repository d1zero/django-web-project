from genres.tests.test_setup import GenreTestSetUp
from ..models import Genre


class GenreTest(GenreTestSetUp):
    def create_genre(self):
        return Genre.objects.create(
            name=self.genre_data['name'],
            description=self.genre_data['description'],
            cover=self.genre_data['cover']
        )

    def test_genre_creation(self):
        genre = self.create_genre()
        self.assertTrue(isinstance(genre, Genre))
        self.assertEqual(str(genre), genre.name)
