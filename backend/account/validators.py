import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


def validate_uzb_phone_number(value):
    if not re.match(r'^\+998\d{9}$', value):
        raise ValidationError(
            _('%(value)s bul O\'zbekistan telefon no\'meri emes'),
            params={'value': value},
        )


def validate_email(value):
    emails = ['test@ihateregex.io', 'test@gmail.com', 'testmail@test.org']
    email_regex = RegexValidator(regex=r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+', message=f"Email format like: {emails}")
    email_regex(value=value)
    return value