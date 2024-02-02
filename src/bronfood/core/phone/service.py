from bronfood.core.phone.exceptions import WrongOtpCode
from bronfood.core.phone.models import (IssueReason, PhoneSmsOtpVerification,
                                        SmsMessage, SmsStatus)
from bronfood.core.phone.utils import generate_otp
from bronfood.core.useraccount.models import UserAccount

INCORRECT_CODE_MESSAGE = (
    'Code: {code} is not as expected. Attempts left: {attempt_count}.'
)
NOT_EXISTS_OR_DECLINED = (
    'There was no otp issued for this number or it was rejected.'
)
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
        sms_status=SmsStatus.PENDING,
        phone_number=user.phone,
        issue_reason=issue_reason
    ).first():
        existing_code.sms_status = SmsStatus.EXPIRED
        existing_code.save()
    return PhoneSmsOtpVerification.objects.create(
        message=message,
        code=generate_otp(user.phone, issue_reason),
        user=user,
        phone_number=user.phone,
        sms_status=SmsStatus.PENDING,
        issue_reason=issue_reason
    )


def validate_otp_verification(
    user: UserAccount, issue_reason: IssueReason, code: str
) -> bool | TypeError | WrongOtpCode:
    if not all(
        (isinstance(user, UserAccount), isinstance(issue_reason, IssueReason),
         isinstance(code, str))
    ):
        raise TypeError(FAILURE_VALIDATE_OTP)
    if existing_code := PhoneSmsOtpVerification.objects.filter(
        sms_status=SmsStatus.PENDING,
        phone_number=user.phone,
        issue_reason=issue_reason
    ).first():
        existing_code.attempt_counter -= 1
        if is_correct := code == existing_code.code:
            existing_code.sms_status = SmsStatus.ACCEPTED
            return existing_code.save() or is_correct
        if not existing_code.attempt_counter:
            existing_code.sms_status = SmsStatus.DECLINED
        existing_code.save()
        raise WrongOtpCode(
            INCORRECT_CODE_MESSAGE.format(
                code=code, attempt_count=existing_code.attempt_counter
            )
        )
    raise WrongOtpCode(NOT_EXISTS_OR_DECLINED)
