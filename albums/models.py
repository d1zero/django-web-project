from django.db import models
from django.utils import timezone
from artists.models import Artist
from tracks.models import Track


class Album(models.Model):
    name = models.TextField(verbose_name='Название альбома')
    artists = models.ManyToManyField(
        Artist, related_name='albums', verbose_name='Исполнители')
    track = models.ManyToManyField(
        Track, related_name='album', verbose_name='Треки')
    date_of_release = models.DateField(
        verbose_name='Дата выпуска', default=timezone.now)
    description = models.TextField(verbose_name='Описание альбома')
    cover = models.ImageField(verbose_name='Обложка',
                              upload_to='images/albums_covers')
    TYPE_OF_ALBUM_CHOICES = [
        ('Сингл', 'Сингл'), ('EP', 'EP'), ('Альбом', 'Альбом')]
    type_of_album = models.CharField(verbose_name='Тип альбома', max_length=6,
                                     choices=(TYPE_OF_ALBUM_CHOICES),
                                     default='Альбом'
                                     )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'
