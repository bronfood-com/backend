from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from bronfood.core.phone.models import PhoneSmsOtpVerification, SmsStatus
from bronfood.core.phone.tasks import check_expired_otps

User = get_user_model()


class CheckExpiredOtpsTest(TestCase):
    '''Класс тестирования проверки просроченных OTP-кодов.'''
    def setUp(self):
        user = User.objects.create_user(
            username='testuser',
            password='12345',
            phone='1234567890'
        )

        PhoneSmsOtpVerification.objects.create(
            user=user,
            expired_at=timezone.now() - timezone.timedelta(minutes=5),
            sms_status=SmsStatus.PENDING,
            issue_reason=1
        )
        PhoneSmsOtpVerification.objects.create(
            user=user,
            expired_at=timezone.now() + timezone.timedelta(minutes=5),
            sms_status=SmsStatus.PENDING,
            issue_reason=1
        )

    def test_check_expired_otps(self):
        check_expired_otps()

        self.assertEqual(
            PhoneSmsOtpVerification.objects.filter(
                sms_status=SmsStatus.EXPIRED
            ).count(),
            1
        )
        self.assertEqual(
            PhoneSmsOtpVerification.objects.filter(
                sms_status=SmsStatus.PENDING
            ).count(),
            1
        )
