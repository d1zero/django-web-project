from django.db import models

class Artist(models.Model):
    nickname = models.CharField(
        verbose_name='Псевдоним', max_length=255, blank=True)
    first_name = models.CharField(
        verbose_name='Имя исполнителя', max_length=255)
    last_name = models.CharField(
        verbose_name='Фамилия исполнителя', max_length=255)
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    photo = models.ImageField(verbose_name='Фото', upload_to='images/artists_photos')
    about = models.TextField(verbose_name='Об исполнителе')

    def __str__(self):
        return str(self.nickname)

    class Meta:
        verbose_name = 'Артист'
        verbose_name_plural = 'Артисты'