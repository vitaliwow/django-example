from core.conf.environ import env

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djangorestframework_camel_case.middleware.CamelCaseMiddleWare",
    "simple_history.middleware.HistoryRequestMiddleware",
]


if not env("DEBUG") and not env("CI", cast=bool, default=False):
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
