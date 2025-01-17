from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.conf import settings
from templated_mail.mail import BaseEmailMessage


class BaseSetEmail(BaseEmailMessage):
    def get_context_data(self) -> dict:
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = self.get_url(context)
        return context

    def get_url(self, context: dict) -> str:
        return settings.ACTIVATION_URL.format(**context)
