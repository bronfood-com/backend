from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class RestaurantOwnerTests(TestCase):

    def test_create_user(self):
        User.objects.create_user(
            role="owner",
            username="Pluto",
            phone="+7(777)5553344"
        )
        owner = User.objects.get(pk=1)
        self.assertEqual(owner.role, "owner")
        self.assertEqual(owner.username, "Pluto")
        self.assertEqual(owner.phone, "+7(777)5553344")
