"""Read .env file"""

import environ  # type: ignore

from core.conf.boilerplate import BASE_DIR

env = environ.Env(
    DEBUG=(bool, False),
    CI=(bool, False),
)

envpath = BASE_DIR / ".env"

if envpath.exists():
    env.read_env(envpath)  # reading .env file

__all__ = [
    "env",
]
