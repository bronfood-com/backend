from django.contrib.auth import get_user_model
from django.test import TestCase

from bronfood.core.phone.models import IssueStatus, PhoneSmsOtpVerification

User = get_user_model()


class PhoneSmsOtpVerificationTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.status = IssueStatus

    def test_verbose_name(self):
        """Проверка verbose name модели PhoneSmsOtpVerification"""
        field_verbose = {
            'password': 'Одноразовый пароль',
            'issue_status': 'Статус выдачи',
            'created_at': 'Создано в',
        }
        for field, expected in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PhoneSmsOtpVerification._meta.get_field(field)
                    .verbose_name, expected
                )

    def test_generate_otp(self):
        """Проверка метода generate_otp модели PhoneSmsOtpVerification."""
        otp_code = PhoneSmsOtpVerification.generate_otp(
            PhoneSmsOtpVerificationTest.user,
            PhoneSmsOtpVerificationTest.status.REGISTRATION
        )
        with self.assertRaises(
            TypeError,
            msg='Ожидается TypeError, при несоответствующем атрибуте user'
        ):
            PhoneSmsOtpVerification.generate_otp(
                user=None,
                issue_status=PhoneSmsOtpVerificationTest.status.REGISTRATION
            )
        with self.assertRaises(
            ValueError,
            msg=('Ожидается ValueError, '
                 'при несоответствующем атрибуте issue_status')
        ):
            PhoneSmsOtpVerification.generate_otp(
                user=PhoneSmsOtpVerificationTest.user,
                issue_status=None
            )
        self.assertEqual(len(otp_code), 4, 'Длина OTP должна быть равна 4.')
        self.assertEqual(
            otp_code,
            str(PhoneSmsOtpVerificationTest.user.otp.last()),
            'Сгенерированный OTP не соответсвует пользователю!'
        )
