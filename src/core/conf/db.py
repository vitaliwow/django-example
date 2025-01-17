from core.conf.environ import env

DATABASES = {
    # read os.environ["DATABASE_URL"] and raises ImproperlyConfigured exception if not found
    "default": env.db(),
}


DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
