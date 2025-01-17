import os.path
from urllib.parse import urlparse, unquote

from rest_framework.exceptions import ValidationError

from apps.videos.models import VideoFile
from core.models.choices import MaterialsCookStatuses


def update_material_status_in_video_file(instance: VideoFile, attr_name: str, status: MaterialsCookStatuses) -> None:
    setattr(instance, attr_name, status)
    instance.save()


def extract_file_name_from_link(link: str) -> str:
    """Return the name of the file from given URL"""
    try:
        parsed_url = urlparse(link)
        file_name = unquote(os.path.basename(parsed_url.path))
        return file_name

    except Exception:
        raise ValidationError("Incorrect link to file")
