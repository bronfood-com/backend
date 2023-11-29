from django.contrib.auth import get_user_model
from django.test import TestCase


class RestaurantOwnerTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="normal@user.com",
            password="foo",
            phone='+7(000) 001-02-03'
        )
        self.assertEqual(user.email, "normal@user.com")

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                password="foo",
                phone='+7(000) 001-02-03'
            )
