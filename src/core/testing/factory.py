import typing as t
from functools import partial

from faker import Faker

from core.testing.mixer import mixer


def register(method: t.Callable) -> t.Callable:
    name = method.__name__
    FixtureRegistry.METHODS[name] = method
    return method


class FixtureRegistry:
    METHODS: dict[str, t.Callable] = {}

    def get(self, name: str) -> t.Callable:
        method = self.METHODS.get(name)
        if not method:
            raise AttributeError(f"Factory method “{name}” not found.")
        return method


class CycleFixtureFactory:
    def __init__(self, factory: "FixtureFactory", count: int) -> None:
        self.factory = factory
        self.count = count

    def __getattr__(self, name: str) -> t.Callable:
        return lambda *args, **kwargs: [getattr(self.factory, name)(*args, **kwargs) for _ in range(self.count)]


class FixtureFactory:
    def __init__(self) -> None:
        self.mixer = mixer
        self.fake = Faker()
        self.registry = FixtureRegistry()

    def __getattr__(self, name: str) -> t.Callable:
        method = self.registry.get(name)
        return partial(method, self)

    def cycle(self, count: int) -> CycleFixtureFactory:
        """
        Run given method X times:
            factory.cycle(5).order()  # gives 5 orders
        """
        return CycleFixtureFactory(self, count)
