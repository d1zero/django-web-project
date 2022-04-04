from django.db import models
from django.utils import timezone
from artists.models import Artist
from genres.models import Genre


class Track(models.Model):
    title = models.TextField(verbose_name='Название трека')
    artists = models.ManyToManyField(Artist, related_name='tracks',
                                     verbose_name='Исполнители')
    date_of_release = models.DateField(
        verbose_name='Дата выпуска', default=timezone.now)
    genres = models.ManyToManyField(Genre, related_name='tracks',
                                    verbose_name='Жанры')
    soundtrack = models.FileField(verbose_name='Саундтрек',
                                  upload_to='tracks/')
    cover = models.ImageField(verbose_name='Обложка',
                              upload_to='images/tracks_covers')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Трек'
        verbose_name_plural = 'Треки'
