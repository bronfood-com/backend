from django.test import TestCase, Client


class UrlTests(TestCase):
    def test_get_restaurants(self):
        """
        Тест проверки получения статуса 200 при get запросе
        на адрес '/restaurants/'
        """
        guest_client = Client()
        response = guest_client.get("/api/restaurants/")
        self.assertEqual(response.status_code, 200)

    def test_get_menu(self):
        """
        Тест проверки получения статуса 200 при get запросе
        на адрес '/menus/'
        """
        guest_client = Client()
        response = guest_client.get("/api/menus/")
        self.assertEqual(response.status_code, 200)
