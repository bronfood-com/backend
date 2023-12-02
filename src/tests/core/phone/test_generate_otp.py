from django.contrib.auth import get_user_model
from django.test import TestCase

from bronfood.core.phone.models import (IssueReason, PhoneSmsOtpVerification,
                                        SmsMessage, SmsStatus)

User = get_user_model()


class GenerateOTPTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.phone_number = '76665554433'
        cls.user = User.objects.create_user(username='auth')
        cls.otp = PhoneSmsOtpVerification.objects.create(
            message=SmsMessage.REGISTRATION,
            user=cls.user,
            phone_number=cls.phone_number,
            sms_status=SmsStatus.PENDING,
            issue_reason=IssueReason.REGISTRATION,
        )

    def test_generate_otp(self):
        """
        Verifying the generate_otp method of the PhoneSmsOtpVerification model.
        """
        self.assertEqual(
            len(GenerateOTPTest.otp.code), 4, 'Длина OTP должна быть равна 4.'
        )
        self.assertEqual(
            GenerateOTPTest.otp.code,
            GenerateOTPTest.user.otp.last().code,
            'Сгенерированный OTP не соответсвует пользователю!'
        )
