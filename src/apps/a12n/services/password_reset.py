from djoser.conf import settings
from templated_mail.mail import BaseEmailMessage

from apps.a12n.services.base import BaseSetEmail


class PasswordResetEmail(BaseSetEmail):
    template_name = "password_reset.html"

    def get_url(self, context: dict) -> str:
        return settings.PASSWORD_RESET_CONFIRM_URL.format(**context)


class PasswordChangedConfirmationEmail(BaseEmailMessage):
    template_name = "password_changed_confirmation.html"
