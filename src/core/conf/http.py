from core.conf.environ import env

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
]

CORS_ALLOW_ALL_ORIGINS = True

DOMAIN = env("DOMAIN", default="")
SITE_NAME = "DOMAIN"

VIDEO_DOWNLOAD_PROXY = env("MY_HTTP_PROXY", default="")
