import typing as t

from faker import Faker
from mixer.backend.django import mixer


class FactoryProtocol(t.Protocol):
    mixer: mixer
    fake: Faker


__all__ = [
    "FactoryProtocol",
]
