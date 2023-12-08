from django.utils.crypto import get_random_string

from bronfood.core.phone.models import PhoneSmsOtpVerification


def generate_otp(sms_status, phone_number):
    while True:
        code = get_random_string(length=4, allowed_chars='0123456789')
        if not PhoneSmsOtpVerification.objects.filter(
            sms_status=sms_status,
            code=code,
            phone_number=phone_number,
        ).exists():
            return code
