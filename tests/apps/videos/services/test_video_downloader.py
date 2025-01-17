import pytest
from apps.videos.models import Video, VideoFile
from apps.videos.services.video.video_downloader import VideoDownloader

pytestmark = [pytest.mark.django_db]


@pytest.mark.skip("Reveal how to mock")
def test_downloader(video: Video) -> None:
    video.setattr_and_save("origin_link", "https://www.youtube.com/watch?v=t4kJ44SXypg")

    video_file: VideoFile = VideoDownloader(video=video)()

    assert video_file.video == video
    assert "media/" in video_file.file.path
    assert video.source in video_file.file.path
    assert video_file.file.path.endswith(".mp4")
