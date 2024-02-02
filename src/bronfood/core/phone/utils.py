from django.utils.crypto import get_random_string

from bronfood.core.phone.models import PhoneSmsOtpVerification, SmsStatus


def generate_otp(phone_number, issue_reason):
    while True:
        code = get_random_string(length=4, allowed_chars='0123456789')
        if not PhoneSmsOtpVerification.objects.filter(
            sms_status=SmsStatus.PENDING,
            code=code,
            phone_number=phone_number,
            issue_reason=issue_reason
        ).exists():
            return code
