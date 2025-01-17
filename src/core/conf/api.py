from datetime import timedelta

from core.conf.environ import env

# Django REST Framework
# https://www.django-rest-framework.org/api-guide/settings/

DISABLE_THROTTLING = env("DISABLE_THROTTLING", cast=bool, default=False)
MAX_PAGE_SIZE = env("MAX_PAGE_SIZE", cast=int, default=1000)
JWT_SECRET_KEY = env("JWT_SECRET_KEY", cast=str, default="secret")
JWT_TOKEN_DATE_FORMAT = "%Y-%m-%d %H:%M:%S %z"  # noqa
BASE_URL = env("BASE_URL", cast=str, default="")
LEN_PRIVATE_LINK = env("LEN_PRIVATE_LINK", cast=int, default=7)
IS_TO_FILTER_QUIZZES = env("IS_TO_FILTER_QUIZZES", cast=bool, default=False)
SA_MEDIA_UPLOADER_SECRET_KEY = env("SA_MEDIA_UPLOADER_SECRET_KEY", cast=str, default="sa-secret-key")
CF_MEDIA_UPLOADER = env("CF_MEDIA_UPLOADER", cast=str, default="cf-media-uploader")
POST_FILE_S3_VERIFY = env("POST_FILE_S3_VERIFY", cast=str, default="dGVzdF9sYXJnZUA=")
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticatedOrReadOnly",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "core.api.renderers.AppJSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "core.api.pagination.AppPagination",
    "PAGE_SIZE": env("PAGE_SIZE", cast=int, default=20),
    "DEFAULT_THROTTLE_RATES": {
        "anon-auth": "10/min",
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "JSON_UNDERSCOREIZE": {
        "no_underscore_before_number": True,
    },
    "EXCEPTION_HANDLER": "core.exceptions.app_service_exception_handler",
}

# Adding session auth and browsable API at the developer machine
if env("DEBUG", cast=bool, default=False):
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].append("rest_framework.authentication.SessionAuthentication")
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    )


# Set up drf_spectacular, https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
    "TITLE": "OPEN API",
    "DESCRIPTION": "So great, needs no docs",
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "CAMELIZE_NAMES": True,
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=35),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "public_id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "TOKEN_OBTAIN_SERIALIZER": "apps.a12n.api.v1.serializers.CustomTokenObtainPairSerializer",
}

DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "#/email/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "LOGOUT_ON_PASSWORD_CHANGE": False,
    "PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "LOGIN_FIELD": "email",
    "EMAIL": {
        "activation": "apps.a12n.services.registration.RegistrationEmail",
        "confirmation": "apps.a12n.services.registration.ConfirmationEmail",
        "password_reset": "apps.a12n.services.password_reset.PasswordResetEmail",
        "password_changed_confirmation": "apps.a12n.services.password_reset.PasswordChangedConfirmationEmail",
    },
    "SERIALIZERS": {
        "current_user": "apps.users.api.v1.serializers.UserMeSerializer",
    },
}
