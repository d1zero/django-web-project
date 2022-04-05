from .test_views_setup import TestSetUp
from ..models import Album
from authentication.models import CustomUser, UserFavorite

class TestAlbumViewSet(TestSetUp):
    def test_get_list_of_albums(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 200)

    def test_get_not_existing_album_by_id(self):
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['message'], 'Album was not found')

    def test_get_existing_album_by_id(self):
        album = Album.objects.create(
            name=self.album_data['name'],
            date_of_release=self.album_data['date_of_release'],
            description=self.album_data['description'],
            cover=self.album_data['cover'],
            type_of_album=self.album_data['type_of_album'],
        )
        album.save()
        self.change_id(album.id)
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 200)


class TestToggleFavoriteAlbumViewSet(TestSetUp):

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

        album = Album.objects.create(
            name=self.album_data['name'],
            date_of_release=self.album_data['date_of_release'],
            description=self.album_data['description'],
            cover=self.album_data['cover'],
            type_of_album=self.album_data['type_of_album'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.albums.add(Album.objects.get(id=album.id))
        favs.save()

        self.client.post(self.favorite_list_url, {'albumId': album.id})
        res = self.client.get(self.favorite_list_url)
        self.assertEqual(res.status_code, 200)

    def test_add_album_to_favorite_with_incorrect_albumId(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        album = Album.objects.create(
            name=self.album_data['name'],
            date_of_release=self.album_data['date_of_release'],
            description=self.album_data['description'],
            cover=self.album_data['cover'],
            type_of_album=self.album_data['type_of_album'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.change_fav_id(album.id)
        res = self.client.post(self.favorite_list_url, {'albumId': 999})
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['message'], 'Album was not found')

    def test_add_album_to_favorite(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        album = Album.objects.create(
            name=self.album_data['name'],
            date_of_release=self.album_data['date_of_release'],
            description=self.album_data['description'],
            cover=self.album_data['cover'],
            type_of_album=self.album_data['type_of_album'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.fav_id = album.id
        res = self.client.post(self.favorite_list_url, {'albumId': album.id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], 'success')

    def test_add_album_to_favorite_without_albumId(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        album = Album.objects.create(
            name=self.album_data['name'],
            date_of_release=self.album_data['date_of_release'],
            description=self.album_data['description'],
            cover=self.album_data['cover'],
            type_of_album=self.album_data['type_of_album'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.change_fav_id(album.id)
        res = self.client.post(self.favorite_list_url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data['message'], 'albumId must not be empty')

    def test_add_and_remove_album_to_favorite_(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        album = Album.objects.create(
            name=self.album_data['name'],
            date_of_release=self.album_data['date_of_release'],
            description=self.album_data['description'],
            cover=self.album_data['cover'],
            type_of_album=self.album_data['type_of_album'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.client.post(self.favorite_list_url, {'albumId': album.id})
        res = self.client.post(self.favorite_list_url, {'albumId': album.id})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], 'success')
        self.assertEqual(len(self.client.get(self.favorite_list_url).data), 0)

    def test_get_favorite_retrieve_without_album(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        album = Album.objects.create(
            name=self.album_data['name'],
            date_of_release=self.album_data['date_of_release'],
            description=self.album_data['description'],
            cover=self.album_data['cover'],
            type_of_album=self.album_data['type_of_album'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.albums.add(Album.objects.get(id=album.id))
        favs.save()

        self.client.post(self.favorite_list_url, {'albumId': album.id})
        res = self.client.get(self.favorite_detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], False)

    def test_get_favorite_retrieve_with_album(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        album = Album.objects.create(
            name=self.album_data['name'],
            date_of_release=self.album_data['date_of_release'],
            description=self.album_data['description'],
            cover=self.album_data['cover'],
            type_of_album=self.album_data['type_of_album'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.albums.add(Album.objects.get(id=album.id))
        favs.save()
        self.change_fav_id(album.id)


        res = self.client.get(self.favorite_detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], True)
