from apps.videos.models import Video
from core.testing import register
from core.testing.types import FactoryProtocol


@register
def user(self: FactoryProtocol, **kwargs: dict) -> Video:
    return self.mixer.blend("users.user", phone_number="1234567", **kwargs)
