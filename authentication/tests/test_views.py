from .test_setup import TestSetUp
from ..models import CustomUser


class TestViews(TestSetUp):
    def test_user_cannot_register_without_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_cannot_register_with_data(self):
        res = self.client.post(self.register_url, self.user_data,
                               format="json")
        self.assertEqual(res.data['message'], 'success')
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_login_without_confirmed_email(self):
        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.data['detail'], 'Email is not confirmed')
        self.assertEqual(res.status_code, 401)

    def test_user_can_login_with_confirmed_email(self):
        self.client.post(self.register_url, self.user_data, format="json")

        user = CustomUser.objects.get(email=self.user_data['email'])
        user.is_active = True
        user.save()

        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertContains(res, 'access')
        self.assertEqual(res.status_code, 200)
