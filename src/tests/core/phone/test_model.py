from django.contrib.auth import get_user_model
from django.test import TestCase

from bronfood.core.phone.models import (IssueReason, PhoneSmsOtpVerification,
                                        SmsMessage, SmsStatus)

User = get_user_model()


class PhoneSmsOtpVerificationTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.phone_number = '76665554433'
        cls.user = User.objects.create_user(
            username='auth', phone=cls.phone_number
        )

    def test_verbose_name(self):
        """Verifying the verbose name of the PhoneSmsOtpVerification model."""
        field_verbose = {
            'message': 'Sms message',
            'code': 'One-time password',
            'phone_number': 'Phone number',
            'sms_status': 'Sms status',
            'issue_reason': 'Code issuance status',
            'created_at': 'Created at',
            'expired_at': 'Expired at',
            'attempt_counter': 'Attempt counter'
        }
        for field, expected in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    PhoneSmsOtpVerification._meta.get_field(field)
                    .verbose_name, expected
                )

    def test_create_object(self):
        field_attrs = {
            'message': SmsMessage.REGISTRATION,
            'user': PhoneSmsOtpVerificationTest.user,
            'phone_number': PhoneSmsOtpVerificationTest.phone_number,
            'sms_status': SmsStatus.PENDING,
            'issue_reason': IssueReason.REGISTRATION
        }
        otp_registration = PhoneSmsOtpVerification.objects.create(
            message=SmsMessage.REGISTRATION,
            user=PhoneSmsOtpVerificationTest.user,
            phone_number=PhoneSmsOtpVerificationTest.phone_number,
            sms_status=SmsStatus.PENDING,
            issue_reason=IssueReason.REGISTRATION,
        )
        for field, expected in field_attrs.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(otp_registration, field), expected
                )
