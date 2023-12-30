from django.core import validators


class FullnameValidator(validators.RegexValidator):
    regex = r'^[А-Яа-яЁёA-Za-z\s]{2,40}$'
    message = (
        "Enter a valid full name. This value may contain only letters "
        "from English and Russian alphabets and spaces. "
        "It must be between 2 and 40 characters."
    )
    flags = 0


class KazakhstanPhoneNumberValidator(validators.RegexValidator):
    regex = r'^7\d{9}$'
    message = (
        'Please enter a phone number starting with 7 followed by 9 digits.'
    )
    flags = 0


class PasswordValidator(validators.RegexValidator):
    regex = r'^[A-Za-z!@#$%^&*()-_+=<>?]{4,20}$'
    message = (
        'Password must be 4 to 20 characters and contain '
        'only Latin letters and the allowed symbols: !@#$%^&*()-_+=<>?'
    )
    flags = 0


class ConfirmationValidator(validators.RegexValidator):
    regex = r'^\d{4}$'
    message = 'Input 4 digits.'
    flags = 0
