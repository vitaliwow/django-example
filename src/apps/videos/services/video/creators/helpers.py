from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.videos.models import Video


def check_is_banned(video: Video) -> bool:
    if video.status == Video.StatusChoices.BANNED:
        raise ValidationError(_("Cannot add previously banned video"))
    return False
