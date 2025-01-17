import factory
from factory import SubFactory

from apps.users.models import User
from apps.videos.models import Video, Transcript, VideoFile
from core.testing import register
from core.testing.types import FactoryProtocol
from tests.factories.apps.playlists import VideoFileFactory


@register
def video(
    self: FactoryProtocol,
    user: User,
    **kwargs: dict,
) -> Video:
    video = self.mixer.blend("videos.Video", uploader=user, **kwargs)
    video.users.add(user)
    video.save()
    return video


class TranscriptVideoFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transcript

    data = factory.Faker("json")
    video_file = SubFactory(VideoFileFactory)
