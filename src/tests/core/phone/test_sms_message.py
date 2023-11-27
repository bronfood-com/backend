import os
from unittest import skipIf

from django.contrib.auth import get_user_model
from django.test import TestCase

from bronfood.core.phone.models import IssueStatus, PhoneSmsOtpVerification
from bronfood.core.phone.sms.sms_message import SMSMessage

User = get_user_model()


class SMSMessageTest(TestCase):
    # TODO: Добавить тест get_sms_backend
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.message = PhoneSmsOtpVerification.generate_otp(
            user=cls.user, issue_status=IssueStatus.REGISTRATION
        )

    @skipIf(os.getenv('ENV_NAME') != 'local', 'Не тестируется в prod.')
    def test_send_message(self):
        self.assertEqual(
            SMSMessage(
                phone_number=87776665544, message=SMSMessageTest.message
            ).send(),
            None
        )
