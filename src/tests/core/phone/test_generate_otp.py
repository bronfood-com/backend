from django.contrib.auth import get_user_model
from django.test import TestCase

from bronfood.core.phone.exceptions import WrongOtpCode
from bronfood.core.phone.models import (IssueReason, PhoneSmsOtpVerification,
                                        SmsMessage, SmsStatus)
from bronfood.core.phone.service import (create_otp_verification,
                                         validate_otp_verification)

User = get_user_model()


class GenerateOTPTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.phone_number = '76665554433'
        cls.user = User.objects.create_user(
            username='auth', phone=cls.phone_number
        )

    def test_create_otp(self):
        otp = create_otp_verification(
            GenerateOTPTest.user, IssueReason.REGISTRATION,
            SmsMessage.REGISTRATION
        )
        self.assertEqual(len(otp.code), 4, 'Длина OTP должна быть равна 4.')
        self.assertEqual(otp.code, GenerateOTPTest.user.otp.last().code,
                         'Сгенерированный OTP не соответсвует пользователю.')
        create_otp_verification(
            GenerateOTPTest.user, IssueReason.REGISTRATION,
            SmsMessage.REGISTRATION
        )
        self.assertEqual(
            PhoneSmsOtpVerification.objects.get(pk=otp.id).sms_status,
            SmsStatus.EXPIRED,
            ('После повторной генерации должен изменится статус предыдущего '
             'кода.')
        )
        self.assertRaises(
            TypeError, create_otp_verification, None, None, None,
            'Ожидается исключение при аргументах с неверным типом данных.'
        )

    def test_validate_otp(self):
        otp = create_otp_verification(
            GenerateOTPTest.user, IssueReason.REGISTRATION,
            SmsMessage.REGISTRATION
        )
        self.assertEqual(
            validate_otp_verification(
                GenerateOTPTest.user, IssueReason.REGISTRATION, otp.code
            ), True,
            'В случае успешной валидации ожидаемый возврат: True.'
        )
        self.assertEqual(
            PhoneSmsOtpVerification.objects.get(pk=otp.id).sms_status,
            SmsStatus.ACCEPTED,
            'После успешной валидации статус OTP кода меняется на ACCEPTED.'
        )
        new_otp = create_otp_verification(
            GenerateOTPTest.user, IssueReason.REGISTRATION,
            SmsMessage.REGISTRATION
        )
        with self.assertRaises(
            WrongOtpCode, msg='Ожидается исключение при неверном OTP коде.'
        ) as error:
            for attempt in range(3):
                try:
                    validate_otp_verification(
                        GenerateOTPTest.user, IssueReason.REGISTRATION, '0000'
                    )
                except Exception as e:
                    if attempt == 2:
                        raise e
        self.assertEqual(
            error.exception.message,
            'Code: 0000 is not as expected. Attempts left: 0.',
            'Неверное сообщение об ошибке после 3 попыток ввода.'
        )
        self.assertEqual(
            PhoneSmsOtpVerification.objects.get(id=new_otp.id).sms_status,
            SmsStatus.DECLINED,
            'После 3 попыток ввода статус OTP кода меняется на DECLINED.'
        )
        with self.assertRaises(
            WrongOtpCode,
            msg='Ожидается исключение, если OTP код не найден или отклонён.'
        ) as error:
            validate_otp_verification(
                GenerateOTPTest.user, IssueReason.REGISTRATION, '0000'
            )
        self.assertEqual(
            error.exception.message,
            'There was no otp issued for this number or it was rejected.',
            'Неверное сообщение об ошибке, '
            'если OTP код не найден или отклонён.'
        )
        with self.assertRaises(
            TypeError,
            msg='Ожидается исключение при аргументах с неверным типом данных.'
        ):
            validate_otp_verification(None, None, None)
