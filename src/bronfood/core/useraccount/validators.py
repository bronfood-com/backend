import re

from django.core import validators
from django.core.exceptions import ValidationError

from bronfood.core.constants import (CONFIRMATION_CODE_LENGTH, DIGITS,
                                     LETTERS_AND_DIGITS, TEMP_DATA_CODE_LENGTH)


class FullnameValidator(validators.RegexValidator):
    regex = r'^[А-Яа-яЁёA-Za-z\s]{2,40}$'
    message = (
        "Enter a valid full name. This value may contain only letters "
        "from English and Russian alphabets and spaces. "
        "It must be between 2 and 40 characters."
    )
    flags = 0


class KazakhstanPhoneNumberValidator(validators.RegexValidator):
    regex = r'^7\d{10}$'
    message = (
        'Please enter a phone number starting with 7 followed by 10 digits.'
    )
    flags = 0


class ConfirmationValidator(validators.RegexValidator):
    regex = r'^\d{4}$'
    message = 'Input 4 digits.'
    flags = 0


def validate_password(value):
    regex = '^[\w@!]+\Z'  # noqa
    if re.search(regex, value) is None:
        unmatch_symbols = ' '.join(set(
            symbol for symbol in value if not re.match(regex, symbol)
        ))
        raise ValidationError(
            'Password error.'
            f'Simbols {unmatch_symbols} are not allowed to be used'
        )
    return value


def validate_temp_data_code(value):
    if len(value) != TEMP_DATA_CODE_LENGTH:
        raise ValidationError(
            f'Temp data code must be exactly {TEMP_DATA_CODE_LENGTH} '
            'characters long.'
        )

    if not all(char in LETTERS_AND_DIGITS for char in value):
        raise ValidationError(
            'Temp data code can only contain letters and digits.'
        )


def validate_confirmation_code(value):
    if len(value) != CONFIRMATION_CODE_LENGTH:
        raise ValidationError(
            f'Confirmation code must be exactly {CONFIRMATION_CODE_LENGTH} '
            'characters long.'
        )

    if not all(char in DIGITS for char in value):
        raise ValidationError(
            'Confirmation code can only contain digits.'
        )
