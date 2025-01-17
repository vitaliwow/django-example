from core.conf.environ import env

DBBACKUP_STORAGE_ACCESS_KEY = env("AWS_ACCESS_KEY_ID", default="")
DBBACKUP_STORAGE_SECRET_KEY = env("AWS_SECRET_ACCESS_KEY", default="")


DBBACKUP_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DBBACKUP_STORAGE_OPTIONS = {
    "access_key": DBBACKUP_STORAGE_ACCESS_KEY,
    "secret_key": DBBACKUP_STORAGE_SECRET_KEY,
    "endpoint_url": "https://storage.yandexcloud.net",
    "bucket_name": "backup",
    "default_acl": "private",
}
DBBACKUP_FILENAME_TEMPLATE = f"{env('SERVER_TYPE')}/" + "{content_type}-{datetime}.{extension}"
DBBACKUP_CLEANUP_KEEP = 10
DBBACKUP_DATE_FORMAT = "%Y-%m-%d-%H:%M"
