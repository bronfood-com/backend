from django.core import validators


class CustomUnicodeUsernameValidator(validators.RegexValidator):
    regex = r"^[А-Яа-яЁёA-Za-z]+(?:[\s][А-Яа-яЁёA-Za-z]+)*$"
    message = (
        "Enter a valid username. This value may contain only letters "
        "from English and Russian alphabets with only one space between words."
    )
    flags = 0
