from .test_views_setup import TestSetUp
from ..models import Artist
from authentication.models import CustomUser, UserFavorite


class TestArtistViewSet(TestSetUp):
    def test_get_list_of_artists(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 200)

    def test_get_not_existing_artist_by_id(self):
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['message'], 'Artist was not found')

    def test_get_existing_artist_by_id(self):
        artist = Artist.objects.create(
            nickname=self.artist_data['nickname'],
            first_name=self.artist_data['first_name'],
            last_name=self.artist_data['last_name'],
            date_of_birth=self.artist_data['date_of_birth'],
            photo=self.artist_data['photo'],
            about=self.artist_data['about'],
        )
        artist.save()
        self.change_id(artist.id)
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 200)


class TestToggleFavoriteArtistViewSet(TestSetUp):

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

        artist = Artist.objects.create(
            nickname=self.artist_data['nickname'],
            first_name=self.artist_data['first_name'],
            last_name=self.artist_data['last_name'],
            date_of_birth=self.artist_data['date_of_birth'],
            photo=self.artist_data['photo'],
            about=self.artist_data['about'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.artists.add(Artist.objects.get(id=artist.id))
        favs.save()

        self.client.post(self.favorite_list_url, {'artistId': artist.id})
        res = self.client.get(self.favorite_list_url)
        self.assertEqual(res.status_code, 200)

    def test_add_artist_to_favorite_with_incorrect_artistId(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        artist = Artist.objects.create(
            nickname=self.artist_data['nickname'],
            first_name=self.artist_data['first_name'],
            last_name=self.artist_data['last_name'],
            date_of_birth=self.artist_data['date_of_birth'],
            photo=self.artist_data['photo'],
            about=self.artist_data['about'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.fav_id = artist.id
        res = self.client.post(self.favorite_list_url, {'artistId': 999})
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['message'], 'Artist was not found')

    def test_add_artist_to_favorite(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        artist = Artist.objects.create(
            nickname=self.artist_data['nickname'],
            first_name=self.artist_data['first_name'],
            last_name=self.artist_data['last_name'],
            date_of_birth=self.artist_data['date_of_birth'],
            photo=self.artist_data['photo'],
            about=self.artist_data['about'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.fav_id = artist.id
        res = self.client.post(self.favorite_list_url, {'artistId': artist.id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], 'success')

    def test_add_artist_to_favorite_without_artistId(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        artist = Artist.objects.create(
            nickname=self.artist_data['nickname'],
            first_name=self.artist_data['first_name'],
            last_name=self.artist_data['last_name'],
            date_of_birth=self.artist_data['date_of_birth'],
            photo=self.artist_data['photo'],
            about=self.artist_data['about'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.change_fav_id(artist.id)
        res = self.client.post(self.favorite_list_url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data['message'], 'artistId must not be empty')

    def test_add_and_remove_artist_to_favorite(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        artist = Artist.objects.create(
            nickname=self.artist_data['nickname'],
            first_name=self.artist_data['first_name'],
            last_name=self.artist_data['last_name'],
            date_of_birth=self.artist_data['date_of_birth'],
            photo=self.artist_data['photo'],
            about=self.artist_data['about'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.client.post(self.favorite_list_url, {'artistId': artist.id})
        res = self.client.post(self.favorite_list_url, {'artistId': artist.id})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], 'success')
        self.assertEqual(len(self.client.get(self.favorite_list_url).data), 0)

    def test_get_favorite_retrieve_without_artist(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        artist = Artist.objects.create(
            nickname=self.artist_data['nickname'],
            first_name=self.artist_data['first_name'],
            last_name=self.artist_data['last_name'],
            date_of_birth=self.artist_data['date_of_birth'],
            photo=self.artist_data['photo'],
            about=self.artist_data['about'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.artists.add(Artist.objects.get(id=artist.id))
        favs.save()

        self.client.post(self.favorite_list_url, {'artistId': artist.id})
        res = self.client.get(self.favorite_detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], False)

    def test_get_favorite_retrieve_with_artist(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        artist = Artist.objects.create(
            nickname=self.artist_data['nickname'],
            first_name=self.artist_data['first_name'],
            last_name=self.artist_data['last_name'],
            date_of_birth=self.artist_data['date_of_birth'],
            photo=self.artist_data['photo'],
            about=self.artist_data['about'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.artists.add(Artist.objects.get(id=artist.id))
        favs.save()
        self.change_fav_id(artist.id)

        res = self.client.get(self.favorite_detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], True)
