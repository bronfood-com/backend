from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def test_healthcheck(self):
        """Тест проверки получения статуса 200 при get запросе
        на адрес '/healthcheck/' """
        guest_client = Client()
        response = guest_client.get('/healthcheck/')
        self.assertEqual(response.status_code, 200)
