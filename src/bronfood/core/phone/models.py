from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

User = get_user_model()


def generate_otp(sms_status, phone_number):
    while True:
        code = get_random_string(length=4, allowed_chars='0123456789')
        if PhoneSmsOtpVerification.objects.filter(
            sms_status=sms_status,
            code=code,
            phone_number=phone_number,
        ).exists():
            continue
        return code


def two_minutes_later():
    return timezone.now() + timezone.timedelta(minutes=2)


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
        verbose_name='Expired at',
        default=two_minutes_later
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.message + self.code

    def save(self, *args, **kwargs) -> None:
        self.code = generate_otp(self.sms_status, self.phone_number)
        return super().save(*args, **kwargs)
