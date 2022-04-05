from .test_models_setup import UserTestSetUp
from ..models import CustomUser


class UserTest(UserTestSetUp):
    def create_user(self):
        return CustomUser.objects.create(email=self.user_data['email'],
                                         username=self.user_data['username'])

    def test_user_creation_without_data(self):
        with self.assertRaisesMessage(TypeError, "create_user() missing 2 required positional arguments: 'email' and 'username'"):
            CustomUser.objects.create_user()

    def test_user_creation_without_username(self):
        with self.assertRaisesMessage(TypeError, "create_user() missing 1 required positional argument: 'username'"):
            CustomUser.objects.create_user(email=self.user_data['email'])

    def test_user_creation_without_email(self):
        with self.assertRaisesMessage(TypeError, "create_user() missing 1 required positional argument: 'email'"):
            CustomUser.objects.create_user(username=self.user_data['username'])

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, CustomUser))
        self.assertEqual(str(user), user.email)

    def test_user_get_image(self):
        user = self.create_user()
        self.assertEqual(user.get_image(), '(Нет изображения)')
        avatar = self.user_data['avatar']
        user.avatar = avatar
        self.assertEqual(user.get_image(), f'<img src="/media/{avatar}" height="100" width="100"/>')

    def test_user_has_perm(self):
        user = self.create_user()
        self.assertEqual(user.has_perm('auth.delete_user'), False)
        user.is_admin = True
        user.save()
        self.assertEqual(user.has_perm('auth.delete_user'), True)

    def test_user_has_module_perms(self):
        user = self.create_user()
        self.assertEqual(user.has_module_perms('auth'), True)
