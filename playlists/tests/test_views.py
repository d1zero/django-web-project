from .test_views_setup import TestSetUp
from ..models import Playlist
from authentication.models import CustomUser, UserFavorite
from tracks.models import Track
from faker import Faker


class TestPlaylistViewSet(TestSetUp):
    def test_get_list_of_playlists(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 200)

    def test_get_not_existing_playlist_by_id(self):
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['message'], 'Playlist was not found')

    def test_get_existing_playlist_by_id(self):
        faker = Faker()
        track = Track.objects.create(
            title=faker.pystr(max_chars=10),
            date_of_release=faker.date_object(),
            soundtrack=faker.pystr(max_chars=10),
            cover=faker.pystr(max_chars=10),
            description=faker.pystr(max_chars=10),
        )
        playlist = Playlist.objects.create(
            name=self.playlist_data['name'],
            description=self.playlist_data['description'],
            photo=self.playlist_data['photo'],
            is_visible=self.playlist_data['is_visible'],
        )
        playlist.track.add(track)
        playlist.save()
        self.change_id(playlist.id)
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 200)


class TestToggleFavoritePlaylistViewSet(TestSetUp):

    def test_get_empty_favorite_list(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        favs = UserFavorite.objects.create(user=user)
        favs.save()

        res = self.client.get(self.favorite_list_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 0)

    def test_get_favorite_list(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        playlist = Playlist.objects.create(
            name=self.playlist_data['name'],
            description=self.playlist_data['description'],
            photo=self.playlist_data['photo'],
            is_visible=self.playlist_data['is_visible'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.playlists.add(Playlist.objects.get(id=playlist.id))
        favs.save()

        self.client.post(self.favorite_list_url, {'playlistId': playlist.id})
        res = self.client.get(self.favorite_list_url)
        self.assertEqual(res.status_code, 200)

    def test_add_playlist_to_favorite_with_incorrect_playlistId(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        playlist = Playlist.objects.create(
            name=self.playlist_data['name'],
            description=self.playlist_data['description'],
            photo=self.playlist_data['photo'],
            is_visible=self.playlist_data['is_visible'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.change_fav_id(playlist.id)
        res = self.client.post(self.favorite_list_url, {'playlistId': 999})
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['message'], 'Playlist was not found')

    def test_add_playlist_to_favorite(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        playlist = Playlist.objects.create(
            name=self.playlist_data['name'],
            description=self.playlist_data['description'],
            photo=self.playlist_data['photo'],
            is_visible=self.playlist_data['is_visible'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.fav_id = playlist.id
        res = self.client.post(self.favorite_list_url, {'playlistId': playlist.id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], 'success')

    def test_add_playlist_to_favorite_without_playlistId(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        playlist = Playlist.objects.create(
            name=self.playlist_data['name'],
            description=self.playlist_data['description'],
            photo=self.playlist_data['photo'],
            is_visible=self.playlist_data['is_visible'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.change_fav_id(playlist.id)
        res = self.client.post(self.favorite_list_url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data['message'], 'playlistId must not be empty')

    def test_add_and_remove_playlist_to_favorite_(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        playlist = Playlist.objects.create(
            name=self.playlist_data['name'],
            description=self.playlist_data['description'],
            photo=self.playlist_data['photo'],
            is_visible=self.playlist_data['is_visible'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.client.post(self.favorite_list_url, {'playlistId': playlist.id})
        res = self.client.post(self.favorite_list_url, {'playlistId': playlist.id})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], 'success')
        self.assertEqual(len(self.client.get(self.favorite_list_url).data), 0)

    def test_get_favorite_retrieve_without_playlist(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        playlist = Playlist.objects.create(
            name=self.playlist_data['name'],
            description=self.playlist_data['description'],
            photo=self.playlist_data['photo'],
            is_visible=self.playlist_data['is_visible'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.playlists.add(Playlist.objects.get(id=playlist.id))
        favs.save()

        self.client.post(self.favorite_list_url, {'playlistId': playlist.id})
        res = self.client.get(self.favorite_detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], False)

    def test_get_favorite_retrieve_with_playlist(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        playlist = Playlist.objects.create(
            name=self.playlist_data['name'],
            description=self.playlist_data['description'],
            photo=self.playlist_data['photo'],
            is_visible=self.playlist_data['is_visible'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.playlists.add(Playlist.objects.get(id=playlist.id))
        favs.save()
        self.change_fav_id(playlist.id)

        res = self.client.get(self.favorite_detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], True)
