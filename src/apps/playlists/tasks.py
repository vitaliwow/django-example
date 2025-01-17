import os

from celery import shared_task

from apps.frames.services.frames_creator import FramesSetCreator
from apps.playlists.models import Playlist
from apps.videos.models import VideoFile
from apps.videos.services.video.video_downloader import VideoDownloader


@shared_task(name="playlists.download_frames_for_all_playlists")
def download_frames_for_commercial_playlists() -> None:
    for playlist in Playlist.objects.only_commercial():
        download_frames_for_playlist.delay(str(playlist.public_id))


@shared_task(name="playlists.download_frames_for_playlist")
def download_frames_for_playlist(playlist_id: str) -> None:
    for video in Playlist.objects.get(pk=playlist_id).videos.exclude_banned().exclude(is_unavailable=True):
        if video.framesets.exists():
            return None

        VideoDownloader(video=video)()
        frameset = FramesSetCreator(video=video)()

        return frameset
