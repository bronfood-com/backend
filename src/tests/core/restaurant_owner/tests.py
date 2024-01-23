from django.test import TestCase
from bronfood.core.restaurant_owner.models import RestaurantOwner


class RestaurantOwnerTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.owner = RestaurantOwner(
            role="owner",
            username="Pluto",
            phone="+7(777)5553344"
        )

    def test_create_user(self):
        self.assertEqual(self.owner.role, "owner")
        self.assertEqual(self.owner.username, "Pluto")
        self.assertEqual(self.owner.phone, "+7(777)5553344")
