from .test_setup import ArtistTestSetUp
from ..models import Artist


class ArtistTest(ArtistTestSetUp):

    def create_artist(self):
        return Artist.objects.create(nickname=self.artist_data['nickname'],
                                     first_name=self.artist_data['first_name'],
                                     last_name=self.artist_data['last_name'],
                                     date_of_birth=self.artist_data['date_of_birth'],
                                     photo=self.artist_data['photo'],
                                     about=self.artist_data['about']
                                     )

    def test_artist_creation(self):
        artist = self.create_artist()
        self.assertTrue(isinstance(artist, Artist))
        self.assertEqual(str(artist), artist.nickname)
