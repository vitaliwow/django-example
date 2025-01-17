import pytest
from apps.playlists.models import Playlist
from apps.users.models import User
from apps.videos.models import Video

pytestmark = [pytest.mark.django_db]


def test_banned_videos_not_in_queryset(video: Video) -> None:
    before = Video.objects.for_viewset().count()
    video.setattr_and_save("status", Video.StatusChoices.BANNED)
    got = Video.objects.for_viewset()
    assert got.count() == before - 1


def test_for_user(video: Video, user: User, staff: User) -> None:
    assert Video.objects.for_user(user=user).count() == 1
    assert Video.objects.for_user(user=staff).count() == 0


@pytest.mark.usefixtures("ya_video")
def test_for_playlist(video: Video, playlist: Playlist) -> None:
    all_videos = Video.objects.count()
    my_video = Video.objects.for_playlist(playlist).count()
    playlist.videos.add(video)

    assert Video.objects.for_playlist(playlist).count() == my_video
    assert Video.objects.count() == all_videos  # noqa: PLR2004
