import typing as t
from dataclasses import dataclass


@dataclass
class Any:
    typeof: t.Any

    def __eq__(self, another: object) -> bool:
        return isinstance(another, self.typeof)
