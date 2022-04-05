from .test_setup import TrackTestSetUp
from ..models import Track


class TrackTest(TrackTestSetUp):
    def create_track(self):
        track = Track.objects.create(
            title=self.track_data['title'],
            date_of_release=self.track_data['date_of_release'],
            soundtrack=self.track_data['soundtrack'],
            cover=self.track_data['cover'],
            description=self.track_data['description'],
        )
        return track

    def test_track_creation(self):
        track = self.create_track()
        self.assertTrue(isinstance(track, Track))
        self.assertEqual(str(track), track.title)
