from django.contrib.auth import get_user_model
from django.test import TestCase

from bronfood.core.phone.models import (IssueReason, PhoneSmsOtpVerification,
                                        SmsMessage, SmsStatus)
from bronfood.core.phone.utils import generate_otp

User = get_user_model()


class GenerateOTPTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.phone_number = '76665554433'
        cls.user = User.objects.create_user(
            username='auth', phone=cls.phone_number
        )
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
        GenerateOTPTest.otp.code = generate_otp(
            SmsStatus.PENDING, GenerateOTPTest.otp.phone_number
        )
        GenerateOTPTest.otp.save()
        self.assertEqual(
            len(GenerateOTPTest.otp.code), 4, 'Длина OTP должна быть равна 4.'
        )
        self.assertEqual(
            GenerateOTPTest.otp.code,
            GenerateOTPTest.user.otp.last().code,
            'Сгенерированный OTP не соответсвует пользователю!'
        )
