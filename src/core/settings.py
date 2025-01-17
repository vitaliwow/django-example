# This file was generated using http://github.com/f213/django starter template.
#
# Settings are split into multiple files using http://github.com/sobolevn/django-split-settings

from split_settings.tools import include

from core.conf.environ import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY", "changeme")
YOUTUBE_API_KEY = env.str("YOUTUBE_API_KEY", "changeme")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)
CI = env.bool("CI", False)

include(
    "conf/ai_server.py",
    "conf/api.py",
    "conf/auth.py",
    "conf/boilerplate.py",
    "conf/db.py",
    "conf/dbbackup.py",
    "conf/email.py",
    "conf/healthchecks.py",
    "conf/http.py",
    "conf/i18n.py",
    "conf/installed_apps.py",
    "conf/media.py",
    "conf/middleware.py",
    "conf/storage.py",
    "conf/sentry.py",
    "conf/static.py",
    "conf/summarization/summarization.py",
    "conf/summarization/segmentors/any_text.py",
    "conf/templates.py",
    "conf/timezone.py",
)
