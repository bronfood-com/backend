from django.test import TestCase


class CoreTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        ...

    def test1(self):
        self.assertTrue(True)
