from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)

generate_token = AccountActivationTokenGenerator()




import re
from django.core.exceptions import ValidationError

def validate_password_strength(password):
    if len(password) <= 5:
        raise ValidationError("Password must be more than 5 characters long.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")
    if not re.search(r'[0-9]', password):
        raise ValidationError("Password must contain at least one number.")