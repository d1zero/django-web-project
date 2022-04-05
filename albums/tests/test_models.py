from .test_setup import AlbumTestSetUp
from ..models import Album


class AlbumTest(AlbumTestSetUp):
    def create_album(self):
        album = Album.objects.create(
            name=self.album_data['name'],
            date_of_release=self.album_data['date_of_release'],
            description=self.album_data['description'],
            cover=self.album_data['cover'],
            type_of_album=self.album_data['type_of_album'],
        )
        return album

    def test_album_creation(self):
        album = self.create_album()
        self.assertTrue(isinstance(album, Album))
        self.assertEqual(str(album), album.name)
