from templated_mail.mail import BaseEmailMessage

from apps.a12n.services.base import BaseSetEmail


class RegistrationEmail(BaseSetEmail):
    template_name = "registration.html"


class ConfirmationEmail(BaseEmailMessage):
    template_name = "confirmation.html"
