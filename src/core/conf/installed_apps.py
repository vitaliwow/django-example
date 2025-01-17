# Application definition

APPS = [
    "core",
    "apps.a12n",
    "apps.frames",
    "apps.playlists",
    "apps.users",
    "apps.videos",
]

THIRD_PARTY_APPS = [
    "dbbackup",
    "django_apscheduler",
    "storages",
    "django_linear_migrations",  # https://adamj.eu/tech/2020/12/10/introducing-django-linear-migrations/
    "django_object_actions",  #  https://github.com/crccheck/django-object-actions
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework_simplejwt",
    "djoser",
    "simple_history",
]

INSTALLED_APPS = APPS + THIRD_PARTY_APPS
