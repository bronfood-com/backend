from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from bronfood.core.phone.constants import SMS_OTP_DURATION_MINUTES


User = get_user_model()


def in_one_hour():
    return timezone.now() + timezone.timedelta(
        minutes=SMS_OTP_DURATION_MINUTES
    )


class IssueReason(models.IntegerChoices):
    REGISTRATION = 1
    PASSWORD_RECOVERY = 2
    EDITING = 3
    PAYMENT_CONFIRMATION = 4


class SmsStatus(models.IntegerChoices):
    PENDING = 1
    ACCEPTED = 2
    DECLINED = 3
    EXPIRED = 4


class SmsMessage(models.TextChoices):
    REGISTRATION = 'Your code for registration in the Broonfood: '
    PASSWORD_RECOVERY = 'Your password recovery code in the Broonfood: '
    EDITING = 'Your code for editing data in the Broonfood: '
    PAYMENT_CONFIRMATION = 'Your payment confirmation code for the Broonfood: '


class PhoneSmsOtpVerification(models.Model):
    """Describing the one-time password model."""
    message = models.CharField(
        verbose_name='Sms message', choices=SmsMessage.choices
    )
    code = models.CharField(
        verbose_name='One-time password', max_length=4
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='otp'
    )
    phone_number = models.CharField(
        verbose_name='Phone number', max_length=11
    )
    sms_status = models.SmallIntegerField(
        verbose_name='Sms status',
        choices=SmsStatus.choices,
        default=SmsStatus.PENDING
    )
    issue_reason = models.SmallIntegerField(
        verbose_name='Code issuance status', choices=IssueReason.choices
    )
    created_at = models.DateTimeField(
        verbose_name='Created at', auto_now_add=True
    )
    expired_at = models.DateTimeField(
        verbose_name='Expired at', default=in_one_hour
    )
    attempt_counter = models.PositiveSmallIntegerField(
        verbose_name='Attempt counter', default=3
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.message + self.code
