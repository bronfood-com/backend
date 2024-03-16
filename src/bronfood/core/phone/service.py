from bronfood.core.phone.exceptions import WrongOtpCode
from bronfood.core.phone.models import (IssueReason, PhoneSmsOtpVerification,
                                        SmsMessage, SmsStatus)
from bronfood.core.phone.utils import generate_otp
from bronfood.core.useraccount.models import UserAccount

INCORRECT_CODE_MESSAGE = 'Code: {code} does not match expected.'
FAILURE_CREATE_OTP = (
    'invalid data type, create_otp_verifacation accepts '
    'arguments like: "UserAccount", "IssueReason", "SmsMessage".'
)
FAILURE_VALIDATE_OTP = (
    'invalid data type, validate_otp_verifacation accepts '
    'arguments like: "UserAccount" and str.'
)


def create_otp_verification(
    user: UserAccount, issue_reason: IssueReason, message: SmsMessage
) -> PhoneSmsOtpVerification | TypeError:
    if not all(
        (isinstance(user, UserAccount), isinstance(issue_reason, IssueReason),
         isinstance(message, SmsMessage))
    ):
        raise TypeError(FAILURE_CREATE_OTP)
    if existing_code := PhoneSmsOtpVerification.objects.filter(
        sms_status=SmsStatus.PENDING, phone_number=user.phone
    ).first():
        existing_code.sms_status = SmsStatus.EXPIRED
        existing_code.save()
    return PhoneSmsOtpVerification.objects.create(
        message=message,
        code=generate_otp(user.phone),
        user=user,
        phone_number=user.phone,
        sms_status=SmsStatus.PENDING,
        issue_reason=issue_reason
    )


def validate_otp_verification(
    user: UserAccount, code: str
) -> bool | TypeError | WrongOtpCode:
    if not all((isinstance(user, UserAccount), isinstance(code, str))):
        raise TypeError(FAILURE_VALIDATE_OTP)
    if existing_code := PhoneSmsOtpVerification.objects.filter(
        sms_status=SmsStatus.PENDING, phone_number=user.phone, code=code
    ).first():
        existing_code.sms_status = SmsStatus.ACCEPTED
        return existing_code.save() or True
    raise WrongOtpCode(INCORRECT_CODE_MESSAGE.format(code=code))
