from celery import shared_task
from .models import Playlist
from tracks.models import Track

@shared_task
def add():
    playlist = Playlist.objects.first()
    playlist.track.clear()
    print(playlist.track.all())
    tracks = Track.objects.all()
    count = 10 if tracks.count() > 10 else tracks.count() // 2
    for _ in range(count):
        track = tracks.order_by('?').first()
        if track not in playlist.track.all():
            playlist.track.add(track)
    print(playlist.track.all())
    playlist.save()
    print('done')