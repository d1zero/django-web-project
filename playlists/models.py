from django.db import models

from tracks.models import Track

class Playlist(models.Model):
    name = models.CharField(verbose_name='Название плейлиста', max_length=40)
    description = models.TextField(verbose_name='Описание плейлиста')
    photo = models.ImageField(verbose_name='Обложка', upload_to='images/playlists_covers')
    track = models.ManyToManyField(Track, related_name='playlist', verbose_name='Треки', blank=True)
    is_visible = models.BooleanField(verbose_name='Отображается?',default=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлист'