from .test_views_setup import TestSetUp
from ..models import Genre
from authentication.models import CustomUser, UserFavorite


class TestGenreViewSet(TestSetUp):
    def test_get_list_of_genres(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 200)

    def test_get_not_existing_genre_by_id(self):
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['message'], 'Genre was not found')

    def test_get_existing_genrem_by_id(self):
        genre = Genre.objects.create(
            name=self.genre_data['name'],
            description=self.genre_data['description'],
            cover=self.genre_data['cover'],
        )
        genre.save()
        self.change_id(genre.id)
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 200)


class TestToggleFavoriteGenreViewSet(TestSetUp):

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

        genre = Genre.objects.create(
            name=self.genre_data['name'],
            description=self.genre_data['description'],
            cover=self.genre_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.genres.add(Genre.objects.get(id=genre.id))
        favs.save()

        self.client.post(self.favorite_list_url, {'genreId': genre.id})
        res = self.client.get(self.favorite_list_url)
        self.assertEqual(res.status_code, 200)

    def test_add_genre_to_favorite_with_incorrect_genreId(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        genre = Genre.objects.create(
            name=self.genre_data['name'],
            description=self.genre_data['description'],
            cover=self.genre_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.change_fav_id(genre.id)
        res = self.client.post(self.favorite_list_url, {'genreId': 999})
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['message'], 'Genre was not found')

    def test_add_genre_to_favorite(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        genre = Genre.objects.create(
            name=self.genre_data['name'],
            description=self.genre_data['description'],
            cover=self.genre_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.fav_id = genre.id
        res = self.client.post(self.favorite_list_url, {'genreId': genre.id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], 'success')

    def test_add_genre_to_favorite_without_genreId(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        genre = Genre.objects.create(
            name=self.genre_data['name'],
            description=self.genre_data['description'],
            cover=self.genre_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.change_fav_id(genre.id)
        res = self.client.post(self.favorite_list_url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data['message'], 'genreId must not be empty')

    def test_add_and_remove_genre_to_favorite_(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        genre = Genre.objects.create(
            name=self.genre_data['name'],
            description=self.genre_data['description'],
            cover=self.genre_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.client.post(self.favorite_list_url, {'genreId': genre.id})
        res = self.client.post(self.favorite_list_url, {'genreId': genre.id})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], 'success')
        self.assertEqual(len(self.client.get(self.favorite_list_url).data), 0)

    def test_get_favorite_retrieve_without_genre(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        genre = Genre.objects.create(
            name=self.genre_data['name'],
            description=self.genre_data['description'],
            cover=self.genre_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.genres.add(Genre.objects.get(id=genre.id))
        favs.save()

        self.client.post(self.favorite_list_url, {'genreId': genre.id})
        res = self.client.get(self.favorite_detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], False)

    def test_get_favorite_retrieve_with_genre(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        genre = Genre.objects.create(
            name=self.genre_data['name'],
            description=self.genre_data['description'],
            cover=self.genre_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.genres.add(Genre.objects.get(id=genre.id))
        favs.save()
        self.change_fav_id(genre.id)

        res = self.client.get(self.favorite_detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], True)
