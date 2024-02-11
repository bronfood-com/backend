from django.urls import reverse

from urllib.parse import urlencode
from rest_framework.test import APITestCase
from bronfood.core.payment_requisites.models import PaymentRequisites
from bronfood.core.client.models import Client


class TestPaymentRequisites(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.test_data_for_card_1 = {
            'card_number': 12345678901234,
            'cardholder_name': 'Test_user_vova',
            'expiration_data': '12/12/2024',
            'cvv': 123
        }
        cls.test_data_for_card_2 = {
            'card_number': 19876543210987,
            'cardholder_name': 'Test_user_nikita',
            'expiration_data': '01/01/2025',
            'cvv': 321
        }
        cls.user_test_1 = Client.objects.create(
            username='test_user_1', phone=89138927124
        )
        cls.user_test_2 = Client.objects.create(
            username='test_user_2', phone=89138927125
        )
        cls.card_with_user_test_1 = PaymentRequisites.objects.create(
            client=cls.user_test_1, **cls.test_data_for_card_1
        )
        cls.card_with_user_test_2 = PaymentRequisites.objects.create(
            client=cls.user_test_2, **cls.test_data_for_card_2
        )
        cls.url_for_user_test_1_detail = reverse(
            'requisites:payment_requisites_detail', kwargs={
                'user_id': cls.user_test_1.id,
                'card_id': cls.card_with_user_test_1.id
            }
        )
        cls.url_for_user_test_2_detail = reverse(
            'requisites:payment_requisites_detail', kwargs={
                'user_id': cls.user_test_2.id,
                'card_id': cls.card_with_user_test_2.id
            }
        )
        query_params = {'save': True}
        query_string = urlencode(query_params)
        cls.url_for_user_test_1_list_with_query_parametr = reverse(
            'requisites:payment_requisites_list', kwargs={
                'user_id': cls.user_test_1.id
            }
        ) + f'?{query_string}'
        cls.url_for_list_for_user_test_1_without_query_parametr = reverse(
            'requisites:payment_requisites_list', kwargs={
                'user_id': cls.user_test_1.id
            }
        )
        cls.url_for_list_for_user_test_2_without_query_parametr = reverse(
            'requisites:payment_requisites_list', kwargs={
                'user_id': cls.user_test_2.id
            }
        )
        cls.test_data_for_card_3 = {
            'card_number': 1987645321098712,
            'cardholder_name': 'Test_user_lena',
            'expiration_data': '02/02/2024',
            'cvv': 456
        }
        cls.test_data_for_updata_card = {
            'card_number': 1000000000000000,
            'cardholder_name': 'Test_user_lena',
            'expiration_data': '02/02/2024',
            'cvv': 987
        }

    def test_get_bank_card_for_concrete_user_when_user_get_his_own_card(self):
        url_1 = self.url_for_user_test_1_detail
        url_2 = self.url_for_user_test_2_detail
        response_for_user_1 = self.client.get(url_1)
        response_for_user_2 = self.client.get(url_2)
        self.assertEqual(200, response_for_user_1.status_code)
        self.assertEqual(200, response_for_user_2.status_code)
        self.assertEqual(
            'Test_user_vova',
            response_for_user_1.data['cardholder_name']
        )
        self.assertEqual(
            'Test_user_nikita',
            response_for_user_2.data['cardholder_name']
        )

    def test_get_bank_card_for_user_when_user_get_not_his_own_card(self):
        url = reverse(
            'requisites:payment_requisites_detail', kwargs={
                'user_id': self.user_test_1.id,
                'card_id': self.card_with_user_test_2.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(400, response.status_code)

    def test_post_user_without_query_parametrs_for_save_card(self):
        count_before_create = PaymentRequisites.objects.count()
        self.client.post(
            self.url_for_list_for_user_test_1_without_query_parametr,
            data=self.test_data_for_card_3
        )
        count_after_create = PaymentRequisites.objects.count()
        self.assertEqual(count_after_create, count_before_create)

    def test_post_user_with_query_parametrs(self):
        count_before_create = PaymentRequisites.objects.count()
        self.client.post(
            self.url_for_user_test_1_list_with_query_parametr,
            data=self.test_data_for_card_3
        )
        count_after_create = PaymentRequisites.objects.count()
        self.assertEqual(count_after_create, count_before_create + 1)

    def test_post_when_try_with_already_exist_card(self):
        response = self.client.post(
            self.url_for_user_test_1_list_with_query_parametr,
            data=self.test_data_for_card_1
        )
        self.assertEqual(400, response.status_code)

    def test_post_when_incorrect_data_in_card_number(self):
        test_data_for_card_1_with_incorrect_data_in_card_number = {
            'card_number': 1987645321098,
            'cardholder_name': 'Test_user_lena',
            'expiration_data': '02/02/2024',
            'cvv': 456
        }
        response = self.client.post(
            self.url_for_user_test_1_list_with_query_parametr,
            data=test_data_for_card_1_with_incorrect_data_in_card_number
        )
        self.assertEqual(
            400,
            response.status_code,
            'В card_number должно быть ровно 16 цифр'
        )

    def test_post_when_incorrect_data_in_cvv(self):
        test_data_for_card_1_with_incorrect_data_in_cvv = {
            'card_number': 19876453210981,
            'cardholder_name': 'Test_user_lena',
            'expiration_data': '02/02/2024',
            'cvv': 4561
        }
        response = self.client.post(
            self.url_for_user_test_1_list_with_query_parametr,
            data=test_data_for_card_1_with_incorrect_data_in_cvv
        )
        self.assertEqual(
            400,
            response.status_code,
            'В cvv не должно быть больше 3 цифр'
        )

    def test_update_data_with_correct_data(self):
        response = self.client.put(
            self.url_for_user_test_1_detail,
            data=self.test_data_for_updata_card
        )
        self.assertEqual(
            200,
            response.status_code
        )

    def test_update_data_with_incorrect_data_card_number(self):
        test_incorrect_data_for_updata_card = {
            'card_number': 100000000000000,
            'cardholder_name': 'Test_user_lena',
            'expiration_data': '02/02/2024',
            'cvv': 987
        }
        response = self.client.put(
            self.url_for_user_test_1_detail,
            data=test_incorrect_data_for_updata_card
        )
        self.assertEqual(
            400,
            response.status_code,
            f'Некорректно передан card_number - '
            f'{test_incorrect_data_for_updata_card["card_number"]}'
        )

    def test_update_data_with_incorrect_data_cvv(self):
        test_incorrect_data_for_updata_card = {
            'card_number': 1000000000000000,
            'cardholder_name': 'Test_user_lena',
            'expiration_data': '02/02/2024',
            'cvv': 9871
        }
        response = self.client.put(
            self.url_for_user_test_1_detail,
            data=test_incorrect_data_for_updata_card
        )
        self.assertEqual(
            400,
            response.status_code,
            f'Некорректно передан cvv - '
            f'{test_incorrect_data_for_updata_card.get("cvv")}'
        )
