from .test_setup import PlaylistTestSetUp
from ..models import Playlist


class PlaylistTest(PlaylistTestSetUp):
    def create_playlist(self):
        playlist = Playlist.objects.create(name=self.playlist_data['name'],
                                           description=self.playlist_data['description'],
                                           photo=self.playlist_data['photo'],
                                           is_visible=self.playlist_data['is_visible'])
        return playlist

    def test_playlist_creation(self):
        playlist = self.create_playlist()
        self.assertTrue(isinstance(playlist, Playlist))
        self.assertEqual(str(playlist), playlist.name)
