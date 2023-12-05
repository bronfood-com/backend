import os
from unittest import skipIf

from django.contrib.auth import get_user_model
from django.test import TestCase

from bronfood.core.phone.models import (IssueReason, PhoneSmsOtpVerification,
                                        SmsMessage, SmsStatus)
from bronfood.core.phone.sms.sms_message import SMSMessage

User = get_user_model()


class SMSMessageTest(TestCase):
    # TODO: Добавить тест get_sms_backend
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.phone_number = '76665554433'
        cls.user = User.objects.create_user(username='auth')
        cls.message = str(PhoneSmsOtpVerification.objects.create(
            message=SmsMessage.REGISTRATION,
            user=cls.user,
            phone_number=cls.phone_number,
            sms_status=SmsStatus.PENDING,
            issue_reason=IssueReason.REGISTRATION,
        ))

    @skipIf(os.getenv('ENV_NAME') != 'local', 'Не тестируется в prod.')
    def test_send_message(self):
        self.assertEqual(
            SMSMessage(phone_number=SMSMessageTest.phone_number,
                       message=SMSMessageTest.message).send(), None
        )
