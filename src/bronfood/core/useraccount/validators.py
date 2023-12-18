from django.core import validators


class UsernameValidator(validators.RegexValidator):
    regex = r"^[А-Яа-яЁёA-Za-z]+(?:[\s][А-Яа-яЁёA-Za-z]+)*$"
    message = (
        "Enter a valid username. This value may contain only letters "
        "from English and Russian alphabets with only one space between words."
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
