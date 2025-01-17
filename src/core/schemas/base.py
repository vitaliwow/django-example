import dataclasses


@dataclasses.dataclass
class DTOWithToDict:
    def to_dict(self) -> dict:
        return {k: v for k, v in dataclasses.asdict(self).items()}  # noqa: C416
