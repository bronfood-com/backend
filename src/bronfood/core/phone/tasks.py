from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from bronfood.core.phone.models import PhoneSmsOtpVerification, SmsStatus


@shared_task
def check_expired_otps():
    '''Задача для проверки просроченных OTP и перевода их в expired.'''
    expired_otps = PhoneSmsOtpVerification.objects.filter(
        expired_at__lte=timezone.now(),
        sms_status__in=[SmsStatus.PENDING, SmsStatus.ACCEPTED]
    )
    expired_otps.update(sms_status=SmsStatus.EXPIRED)
