import typing as t
from datetime import datetime, timedelta

import factory

from apps.interactions.models import Quiz
from apps.playlists.models import Category, Playlist, PrivateLink, PrivateLinksForUsers, GPTExpensesReport
from apps.summarization.models import Timecodes, Summary, ShortSummary
from apps.users.models import User
from apps.videos.models import Video, VideoFile, Transcript
from core.testing import register
from core.testing.types import FactoryProtocol
from factory import fuzzy, SubFactory
from pytz import UTC


class VideoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Video

    video_id = factory.Sequence(lambda n: f"video_{n:04d}")
    title = factory.Faker("sentence", nb_words=6)
    description = factory.Faker("paragraph", nb_sentences=3)
    duration = factory.Faker("random_int", min=0, max=10000)


class VideoFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VideoFile

    file = factory.Faker("file_name", category="video")
    ogg = factory.Faker("file_name", category="audio")


class TimecodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Timecodes

    raw_data = factory.Faker("json")
    data = factory.Faker("json")
    videofile = SubFactory(VideoFileFactory)
    video = SubFactory(VideoFactory)
    purpose = factory.Faker("random_element", elements=[x[0] for x in Timecodes.Purpose.choices])


class TranscriptFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transcript

    data = factory.Faker("json")
    video = SubFactory(VideoFactory)
    video_file = SubFactory(VideoFileFactory)


class SummaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Summary

    timecodes = SubFactory(TimecodeFactory)
    raw_data = factory.Faker('json')
    pdf_file = factory.django.FileField(filename="example.pdf")
    video = SubFactory(VideoFactory)
    video_file = SubFactory(VideoFileFactory)


class ShortSummaryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShortSummary

    full_summary = SubFactory(SummaryFactory)
    data = factory.Faker('json')
    video_file = SubFactory(VideoFileFactory)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = True
    is_superuser = True
    email = factory.Faker("email")
    password = "passw0rd!"


@register
def playlist(
    self: FactoryProtocol,
    user: User,
    privacy_type: Playlist.PrivacyTypeChoices = Playlist.PrivacyTypeChoices.PUBLIC,
    videos: list | None = None,
    *args: t.Any,
    **kwargs: dict,
) -> Video:
    return self.mixer.blend(
        "playlists.Playlist",
        *args,
        owner=user,
        videos=videos if videos else [],
        privacy_type=privacy_type,
        **kwargs,
    )


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = fuzzy.FuzzyChoice([el for el in Category.CategoryChoices.choices])


class PlaylistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Playlist

    owner = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    privacy_type = fuzzy.FuzzyChoice([el for el in Playlist.PrivacyTypeChoices.choices])


class QuizFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quiz

    data = factory.Faker("json")
    playlist = SubFactory(PlaylistFactory)
    video = SubFactory(VideoFactory)
    video_file = SubFactory(VideoFileFactory)


class PrivateLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PrivateLink

    playlist = factory.SubFactory(PlaylistFactory)
    lifetime = fuzzy.FuzzyDateTime(datetime.now(tz=UTC), datetime.now(tz=UTC) + timedelta(days=30))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        lifetime = datetime.isoformat(kwargs["lifetime"])
        to_encrypt = {
            "user_id": str(kwargs["playlist"].owner_id),
            "playlist_pk": str(kwargs["playlist"].pk),
            "lifetime": lifetime,
        }
        token = PrivateLink._create_token(to_encrypt)
        kwargs["token"] = token
        kwargs["hash"] = PrivateLink._create_hash()

        obj = model_class(*args, **kwargs)
        obj.save()
        return obj


class PrivateLinksForUsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PrivateLinksForUsers

    private_link = SubFactory(PrivateLinkFactory)
    user = SubFactory(UserFactory)


class GPTExpensesReportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GPTExpensesReport

    units_spent = factory.Faker('pyint', min_value=0, max_value=1000)
    type_operation = factory.Faker(
        "random_element", elements=[x[0] for x in GPTExpensesReport.OperationTypeChoices.choices]
    )
    api_request = 'yandex-gpt'
    user = SubFactory(UserFactory)
    video = SubFactory(VideoFactory)
    playlist = SubFactory(PlaylistFactory)
