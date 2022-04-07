# from .test_views_setup import TestSetUp
# from ..models import CustomUser


# class TestRegisterView(TestSetUp):
#     def test_user_cannot_register_without_data(self):
#         res = self.client.post(self.register_url)
#         self.assertEqual(res.data['email'], ['Email must not be empty'])
#         self.assertEqual(res.data['username'], ['Username must not be empty'])
#         self.assertEqual(res.data['password'], ['Password must not be empty'])
#         self.assertEqual(res.status_code, 400)

#     def test_user_cannot_register_with_used_email(self):
#         self.client.post(self.register_url, self.user_data,
#                          format="json")
#         res = self.client.post(self.register_url, {'email': self.user_data['email'],
#                                                    'username': self.faker.simple_profile()['username'],
#                                                    'password': self.user_data['password']},
#                                format="json")
#         self.assertEqual(res.data['email'], ['User with this email already exists'])
#         self.assertEqual(res.status_code, 400)

#     def test_user_cannot_register_with_used_username(self):
#         self.client.post(self.register_url, self.user_data,
#                          format="json")
#         res = self.client.post(self.register_url, {'email': self.faker.email(),
#                                                    'username': self.user_data['username'],
#                                                    'password': self.user_data['password']},
#                                format="json")
#         self.assertEqual(res.data['username'], ['User with this username already exists'])
#         self.assertEqual(res.status_code, 400)

#     def test_user_cannot_register_with_short_password(self):
#         res = self.client.post(self.register_url, {'email': self.user_data['email'],
#                                                    'username': self.user_data['username'],
#                                                    'password': self.faker.password(length=7)},
#                                format="json")
#         self.assertEqual(res.data['password'], ['Password is too short'])
#         self.assertEqual(res.status_code, 400)

#     def test_user_can_register_with_data(self):
#         res = self.client.post(self.register_url, self.user_data,
#                                format="json")
#         self.assertEqual(res.data['message'], 'success')
#         self.assertEqual(res.status_code, 201)


# class TestLoginView(TestSetUp):
#     def test_user_cannot_login_without_data(self):
#         self.client.post(self.register_url, self.user_data, format="json")
#         res = self.client.post(self.login_url)
#         self.assertEqual(res.data['email'], ['Email must be provided'])
#         self.assertEqual(res.data['password'], ['Password must be provided'])
#         self.assertEqual(res.status_code, 400)

#     def test_user_cannot_login_without_email(self):
#         self.client.post(self.register_url, self.user_data, format="json")
#         res = self.client.post(self.login_url, {'password': self.user_data['password']})
#         self.assertEqual(res.data['email'], ['Email must be provided'])
#         self.assertEqual(res.status_code, 400)

#     def test_user_cannot_login_without_password(self):
#         self.client.post(self.register_url, self.user_data, format="json")
#         res = self.client.post(self.login_url, {'email': self.user_data['email']})
#         self.assertEqual(res.data['password'], ['Password must be provided'])
#         self.assertEqual(res.status_code, 400)

#     def test_user_cannot_login_does_not_exist(self):
#         res = self.client.post(self.login_url, self.user_data, format="json")
#         self.assertEqual(res.data['message'], 'User with provided credentials does not exist')
#         self.assertEqual(res.status_code, 404)

#     def test_user_cannot_login_without_confirmed_email(self):
#         self.client.post(self.register_url, self.user_data, format="json")
#         res = self.client.post(self.login_url, self.user_data, format="json")
#         self.assertEqual(res.data['message'], 'Email is not confirmed')
#         self.assertEqual(res.status_code, 401)

#     def test_user_cannot_login_with_incorrect_password(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         res = self.client.post(self.login_url, {'email': self.user_data['email'],
#                                                 'password': self.user_data['password'] + 'a'
#                                                 }, format="json")
#         self.assertEqual(res.data['message'], 'Incorrect password')
#         self.assertEqual(res.status_code, 401)

#     def test_user_can_login_with_confirmed_email(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         res = self.client.post(self.login_url, self.user_data, format="json")
#         self.assertContains(res, 'access')
#         self.assertEqual(res.status_code, 200)


# class TestLogoutView(TestSetUp):
#     def test_user_cannot_logout_without_bearer(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         logout_res = self.client.post(self.logout_url)
#         self.assertEqual(logout_res.status_code, 401)

#     def test_user_cannot_logout_without_cookie(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         login_res = self.client.post(self.login_url, self.user_data, format="json")
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])
#         self.client.cookies.clear()
#         logout_res = self.client.post(self.logout_url)
#         self.assertEqual(logout_res.data['message'], 'Unauthenticated')
#         self.assertEqual(logout_res.status_code, 401)

#     def test_user_cannot_logout_with_empty_cookie(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         login_res = self.client.post(self.login_url, self.user_data, format="json")
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])
#         self.client.cookies['refresh'] = ''
#         logout_res = self.client.post(self.logout_url)
#         self.assertEqual(logout_res.data['message'], 'Unauthenticated')
#         self.assertEqual(logout_res.status_code, 401)

#     def test_user_cannot_logout_cookie_not_valid(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         login_res = self.client.post(self.login_url, self.user_data, format="json")
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])
#         self.client.cookies['refresh'] = 'asdasdas'
#         logout_res = self.client.post(self.logout_url)
#         self.assertEqual(logout_res.data['message'], 'Cookie is not valid')
#         self.assertEqual(logout_res.status_code, 401)

#     def test_user_can_logout(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         login_res = self.client.post(self.login_url, self.user_data, format="json")
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])
#         logout_res = self.client.post(self.logout_url)
#         self.assertEqual(logout_res.data['message'], 'success')
#         self.assertEqual(logout_res.status_code, 200)


# class TestUserView(TestSetUp):
#     def test_user_cannot_get_user_data_without_bearer(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         user_res = self.client.get(self.user_url)
#         self.assertEqual(user_res.status_code, 401)

#     def test_get_user_data(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         login_res = self.client.post(self.login_url, self.user_data, format="json")
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])
#         user_res = self.client.get(self.user_url)
#         self.assertEqual(user_res.data['id'], user.id)
#         self.assertEqual(user_res.data['email'], user.email)
#         self.assertEqual(user_res.data['username'], user.username)
#         self.assertEqual(user_res.status_code, 200)


# class TestUserConfirmAPIView(TestSetUp):
#     def test_user_confirm_with_bad_token(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])

#         res = self.client.patch(self.confirm_url + user.token + 'a')
#         self.assertEqual(res.data['message'], 'Codes are different')
#         self.assertEqual(res.status_code, 401)

#     def test_user_confirm(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])

#         res = self.client.patch(self.confirm_url + user.token)
#         self.assertEqual(res.data['message'], 'success')
#         self.assertEqual(res.status_code, 200)


# class TestUserUpdate(TestSetUp):
#     def test_user_cannot_update_data_without_bearer(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         res = self.client.patch(self.update_url)
#         self.assertEqual(res.status_code, 401)

#     def test_user_cannot_update_data_without_data(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         login_res = self.client.post(self.login_url, self.user_data, format="json")
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])
#         res = self.client.patch(self.update_url)
#         self.assertEqual(res.status_code, 200)

#     def test_user_cannot_update_data_with_empty_username(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         login_res = self.client.post(self.login_url, self.user_data, format="json")
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])
#         res = self.client.patch(self.update_url, {'username': ''}, format="json")
#         self.assertEqual(res.status_code, 200)

#     def test_user_cannot_update_data_with_used_username(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         login_res = self.client.post(self.login_url, self.user_data, format="json")
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])
#         res = self.client.patch(self.update_url, {'username': user.username}, format="json")
#         self.assertEqual(res.data['message'], 'Username already taken')
#         self.assertEqual(res.status_code, 400)

#     def test_user_can_update_data_with_new_username(self):
#         self.client.post(self.register_url, self.user_data, format="json")

#         user = CustomUser.objects.get(email=self.user_data['email'])
#         user.is_active = True
#         user.save()

#         login_res = self.client.post(self.login_url, self.user_data, format="json")
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_res.data['access'])
#         res = self.client.patch(self.update_url, data={'username': self.faker.pystr()}, format="json")
#         self.assertEqual(res.status_code, 200)
