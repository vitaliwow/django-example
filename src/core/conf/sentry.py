from core.conf.environ import env

SENTRY_DSN = env("SENTRY_DSN", cast=str, default="")

if not env("DEBUG") and len(SENTRY_DSN):
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.redis import RedisIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration(monitor_beat_tasks=True), RedisIntegration()],
        traces_sample_rate=0.8,
        send_default_pii=True,
        environment=env("SERVER_TYPE", cast=str, default="test"),
    )
