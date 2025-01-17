import typing as t

import pytest
from apps.users.models import User
from apps.videos.models import Video
from apps.videos.services.video.video_updater import VideoUpdater
from core.models.choices import PurposeChoices
from rest_framework.exceptions import ValidationError

pytestmark = [pytest.mark.django_db]


def test_update_without_data_not_fails(video: Video, staff: User) -> None:
    VideoUpdater(data={}, instance=video, user=staff)()


@pytest.mark.parametrize(
    ("field_name", "initial", "expected"),
    [
        ("title", "Initial", "Final"),
        ("description", "Old", "New"),
        ("is_banned", False, True),
        ("purpose", PurposeChoices.PERSONAL, PurposeChoices.EDUCATIONAL),
    ],
)
def test_update(video: Video, staff: User, field_name: str, initial: t.Any, expected: t.Any) -> None:
    video.setattr_and_save(field_name, initial)

    upd_video = VideoUpdater(data={field_name: expected}, instance=video, user=staff)()

    assert video.pk == upd_video.pk
    assert getattr(video, field_name) == expected


def test_user_cant_update_video(video: Video, user: User) -> None:
    with pytest.raises(ValidationError, match="Only staff can update video"):
        VideoUpdater(data={}, instance=video, user=user)()


def test_update_with_anon(anon_user: User, video: Video) -> None:
    with pytest.raises(ValidationError, match="Only staff can update video"):
        VideoUpdater(data={}, instance=video, user=anon_user)()
