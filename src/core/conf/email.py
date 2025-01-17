from core.conf.environ import env

EMAIL_HOST = env("EMAIL_HOSTER", cast=str, default="")
EMAIL_PORT = env("HOST_EMAIL_PORT", cast=int, default="")
EMAIL_HOST_USER = env("APP_EMAIL", cast=str, default="")
EMAIL_HOST_PASSWORD = env("APP_EMAIL_PASSWORD", cast=str, default="")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = True
