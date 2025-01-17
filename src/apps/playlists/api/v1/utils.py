from datetime import datetime
from typing import Any

import jwt

from core.conf.api import JWT_SECRET_KEY, JWT_TOKEN_DATE_FORMAT


def jwt_encode_dict(encoding_data: dict[str, Any]) -> str:
    return jwt.encode(encoding_data, JWT_SECRET_KEY)


def jwt_decode_dict(encoded_data: str) -> dict[str, Any]:
    return jwt.decode(encoded_data, JWT_SECRET_KEY, algorithms=["HS256"])


def get_token_expiration_time(lifetime: datetime) -> str:
    return convert_datetime_to_str(lifetime)


def convert_str_to_datetime(date_time: str) -> datetime:
    return datetime.strptime(date_time, JWT_TOKEN_DATE_FORMAT)  # noqa: DTZ007


def convert_datetime_to_str(date_time: datetime) -> str:
    return datetime.strftime(date_time, JWT_TOKEN_DATE_FORMAT)
