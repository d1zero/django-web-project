from django.db import models

class Genre(models.Model):
    name = models.CharField(verbose_name='Название плейлиста', max_length=255)
    description = models.TextField(verbose_name='Описание жанра')
    cover = models.ImageField(verbose_name='Обложка', upload_to='images/genres_covers')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'