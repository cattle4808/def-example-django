import re
from rest_framework.exceptions import ValidationError

GLOBAL_PHONE_REGEX = re.compile(r'^\+?[1-9]\d{1,14}$')
INVALID_CHARS_REGEX = re.compile(r'[^\d\+\-\(\)\s]')

def validate_phone_number(value):
    """
    Validates a phone number for global formats (E.164 standard).
    """
    normalized_value = re.sub(r'[\s\-()]+', '', value)

    if INVALID_CHARS_REGEX.search(value):
        raise ValidationError(f"The phone number contains invalid characters: {value}")

    if not GLOBAL_PHONE_REGEX.match(normalized_value):
        raise ValidationError(f"Invalid phone number format: {value}")

    return normalized_value
