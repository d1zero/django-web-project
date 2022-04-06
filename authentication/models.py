from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from simple_history.models import HistoricalRecords
from django.utils.html import mark_safe
from albums.models import Album
from artists.models import Artist
from genres.models import Genre
from playlists.models import Playlist
from tracks.models import Track


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        favs = UserFavorite.objects.create(user=user)
        favs.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=60,
                              unique=True)
    username = models.CharField(verbose_name='Имя пользователя',
                                max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='Дата создания',
                                       auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Последний вход',
                                      auto_now=True)
    avatar = models.ImageField(upload_to='images/users_avatars/',
                               verbose_name='Аваратка', blank=True)
    token = models.TextField(verbose_name='Register token')

    def get_image(self):
        if self.avatar:
            return mark_safe(
                f'<img src="{self.avatar.url}" height="100" width="100"/>'
            )
        else:
            return '(Нет изображения)'

    get_image.short_description = 'Аватар'
    get_image.allow_tags = True

    is_active = models.BooleanField(verbose_name='Активирован', default=False)
    is_admin = models.BooleanField(default=False, verbose_name='Администратор')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()
    history = HistoricalRecords()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserFavorite(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track, related_name='favorite_tracks')
    albums = models.ManyToManyField(Album, related_name='favorite_albums')
    artists = models.ManyToManyField(Artist, related_name='favorite_artists')
    playlists = models.ManyToManyField(Playlist,
                                       related_name='favorite_playlists')
    genres = models.ManyToManyField(Genre, related_name='favorite_genres')

    def __str__(self):
        return f"{self.user.username}'s Favorites"

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
