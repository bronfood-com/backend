from random import randint

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


MIN_OTP_VALUE = 1
MAX_OTP_VALUE = 9999
MIN_OTP_MESSAGE = 'Значение должно быть больше 0.'
MAX_OTP_MESSAGE = 'Значение должно быть меньше 10000'

GENERATE_TYPE_ERROR = 'Expected an instance of User, but got {type}'
GENERATE_VALUE_ERROR = '{issue_status} is not a valid IssueStatus'


class IssueStatus(models.IntegerChoices):
    REGISTRATION = 1
    PASSWORD_RECOVERY = 2
    EDITING = 3
    PAYMENT_CONFIRMATION = 4


class PhoneSmsOtpVerification(models.Model):
    """Класс описывающий модель одноразовых паролей."""
    password = models.IntegerField(
        verbose_name='Одноразовый пароль',
        validators=[
            MinValueValidator(MIN_OTP_VALUE, message=MIN_OTP_MESSAGE),
            MaxValueValidator(MAX_OTP_VALUE, message=MAX_OTP_MESSAGE)
        ]
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='otp'
    )
    issue_status = models.IntegerField(
        verbose_name='Статус выдачи', choices=IssueStatus.choices
    )
    created_at = models.DateTimeField(
        verbose_name='Создано в', auto_now_add=True
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.password).zfill(4)

    @staticmethod
    def generate_otp(user: User, issue_status: IssueStatus) -> str:
        """Генерирует одноразовый пароль."""
        if not isinstance(user, User):
            raise TypeError(
                GENERATE_TYPE_ERROR.format(type=type(user).__name__)
            )
        if issue_status not in IssueStatus.values:
            raise ValueError(
                GENERATE_VALUE_ERROR.format(issue_status=issue_status)
            )
        return str(PhoneSmsOtpVerification.objects.create(
            password=randint(MIN_OTP_VALUE, MAX_OTP_VALUE),
            user=user,
            issue_status=issue_status
        ))
