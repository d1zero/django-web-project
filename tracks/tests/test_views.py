from .test_views_setup import TestSetUp
from ..models import Track
from authentication.models import CustomUser, UserFavorite

class TestTrackViewSet(TestSetUp):
    def test_get_list_of_tracks(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 200)

    def test_get_not_existing_track_by_id(self):
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['message'], 'Track was not found')

    def test_get_existing_track_by_id(self):
        track = Track.objects.create(
            title=self.track_data['title'],
            date_of_release=self.track_data['date_of_release'],
            soundtrack=self.track_data['soundtrack'],
            description=self.track_data['description'],
            cover=self.track_data['cover'],
        )
        track.save()
        self.change_id(track.id)
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, 200)


class TestToggleFavoriteTrackViewSet(TestSetUp):

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

        track = Track.objects.create(
            title=self.track_data['title'],
            date_of_release=self.track_data['date_of_release'],
            soundtrack=self.track_data['soundtrack'],
            description=self.track_data['description'],
            cover=self.track_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.tracks.add(Track.objects.get(id=track.id))
        favs.save()

        self.client.post(self.favorite_list_url, {'trackId': track.id})
        res = self.client.get(self.favorite_list_url)
        self.assertEqual(res.status_code, 200)

    def test_add_track_to_favorite_with_incorrect_trackId(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        track = Track.objects.create(
            title=self.track_data['title'],
            date_of_release=self.track_data['date_of_release'],
            soundtrack=self.track_data['soundtrack'],
            description=self.track_data['description'],
            cover=self.track_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.change_fav_id(track.id)
        res = self.client.post(self.favorite_list_url, {'trackId': 999})
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.data['message'], 'Track was not found')

    def test_add_track_to_favorite(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        track = Track.objects.create(
            title=self.track_data['title'],
            date_of_release=self.track_data['date_of_release'],
            soundtrack=self.track_data['soundtrack'],
            description=self.track_data['description'],
            cover=self.track_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.fav_id = track.id
        res = self.client.post(self.favorite_list_url, {'trackId': track.id})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], 'success')

    def test_add_track_to_favorite_without_trackId(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        track = Track.objects.create(
            title=self.track_data['title'],
            date_of_release=self.track_data['date_of_release'],
            soundtrack=self.track_data['soundtrack'],
            description=self.track_data['description'],
            cover=self.track_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.change_fav_id(track.id)
        res = self.client.post(self.favorite_list_url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data['message'], 'trackId must not be empty')

    def test_add_and_remove_track_to_favorite_(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        track = Track.objects.create(
            title=self.track_data['title'],
            date_of_release=self.track_data['date_of_release'],
            soundtrack=self.track_data['soundtrack'],
            description=self.track_data['description'],
            cover=self.track_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.save()

        self.client.post(self.favorite_list_url, {'trackId': track.id})
        res = self.client.post(self.favorite_list_url, {'trackId': track.id})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], 'success')
        self.assertEqual(len(self.client.get(self.favorite_list_url).data), 0)

    def test_get_favorite_retrieve_without_track(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        track = Track.objects.create(
            title=self.track_data['title'],
            date_of_release=self.track_data['date_of_release'],
            soundtrack=self.track_data['soundtrack'],
            description=self.track_data['description'],
            cover=self.track_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.tracks.add(Track.objects.get(id=track.id))
        favs.save()

        self.client.post(self.favorite_list_url, {'trackId': track.id})
        res = self.client.get(self.favorite_detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], False)

    def test_get_favorite_retrieve_with_track(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])

        track = Track.objects.create(
            title=self.track_data['title'],
            date_of_release=self.track_data['date_of_release'],
            soundtrack=self.track_data['soundtrack'],
            description=self.track_data['description'],
            cover=self.track_data['cover'],
        )
        favs = UserFavorite.objects.create(user=user)
        favs.tracks.add(Track.objects.get(id=track.id))
        favs.save()
        self.change_fav_id(track.id)


        res = self.client.get(self.favorite_detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message'], True)
