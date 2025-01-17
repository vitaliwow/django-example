import pytest

from apps.playlists.models import Playlist
from apps.summarization.models import Timecodes, Summary
from apps.summarization.tasks.quizzes import create_quiz_from_timecodes
from apps.users.models import User
from apps.videos.models import Video

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures("mocked_quiz_generator", "mocked_filtering_quiz_generator", "mocked_quiz_expenses")
def test_create_quiz_from_timecodes(
    full_summary_from_video_file: Summary, user: User, ya_video: Video, playlist: Playlist
) -> None:
    timecodes = Timecodes.objects.create(data={"timecodes": [1, 2, 3]}, video=ya_video)
    full_summary_from_video_file.timecodes = timecodes
    full_summary_from_video_file.save()

    create_quiz_from_timecodes(timecodes.pk, user.pk)
