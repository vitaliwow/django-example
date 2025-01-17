import boto3
from django.core.files.storage import FileSystemStorage

from core.conf.environ import env

AWS_S3_ENDPOINT_URL = "https://storage.yandexcloud.net"
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="")
AWS_DEFAULT_ACL = "public-read"
AWS_S3_REGION_NAME = "ru-central1"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.storage.yandexcloud.net"
DEFAULT_FILE_STORAGE_HOST = env("DEFAULT_FILE_STORAGE", cast=str, default="django.core.files.storage.FileSystemStorage")
DEFAULT_STATICFILES_STORAGE = env(
    "DEFAULT_STATIC_STORAGE",
    cast=str,
    default="django.contrib.staticfiles.storage.StaticFilesStorage",
)
LOGS_BUCKET_NAME = env("LOGS_BUCKET_NAME", default="")
MEDIA_BUCKET_NAME = env("MEDIA_BUCKET_NAME", default="")

FRAMES_DIR = env("FRAMES_DIR", cast=str, default="/tmp/videos/frames/")  # noqa: S108
VIDEO_FILES_PATH = env("VIDEO_FILES_PATH", cast=str, default="/tmp/videos/")  # noqa: S108

STORAGES = {
    "default": {
        "BACKEND": DEFAULT_FILE_STORAGE_HOST,
    },
    "staticfiles": {
        "BACKEND": DEFAULT_STATICFILES_STORAGE,
    },
}


class LocalStorage(FileSystemStorage):
    def __init__(self, location: str | None = None, base_url: str | None = None) -> None:
        if location is None:
            location = FRAMES_DIR
        if base_url is None:
            base_url = "/frames/"
        super().__init__(location, base_url)


s3_client = boto3.client(
    service_name="s3",
    endpoint_url=AWS_S3_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME,
)


def send_file_to_s3(file_name: str, file_content: str) -> None:
    s3_client.put_object(Bucket=LOGS_BUCKET_NAME, Key=file_name, Body=file_content.encode("utf-8"))


def get_file_s3(key: str, bucket_id: str | None = None):
    if bucket_id is None:
        bucket_id = MEDIA_BUCKET_NAME
    return s3_client.get_object(Bucket=bucket_id, Key=key)
