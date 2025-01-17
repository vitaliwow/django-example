import logging
import typing as t
from abc import ABCMeta, abstractmethod


class BaseService(metaclass=ABCMeta):
    """This is a template of a base service.
    All services in the app should follow this rules:
      * Input variables should be done at the __init__ phase
      * Service should implement a single entrypoint without arguments

    This is ok:
      @dataclass
      class UserCreator(BaseService):
        first_name: str
        last_name: Optional[str]

        def act(self) -> User:
          return User.objects.create(first_name=self.first_name, last_name=self.last_name)

        # user = UserCreator(first_name="Ivan", last_name="Petrov")()

    This is not ok:
      class UserCreator:
        def __call__(self, first_name: str, last_name: Optional[str]) -> User:
          return User.objects.create(first_name=self.first_name, last_name=self.last_name)

    For more implementation examples,
    check out https://github.com/tough-dev-school/education-backend/tree/master/src/orders/services
    """

    def __call__(self) -> t.Any:
        self.validate()
        try:
            result = self.act()
        except Exception as ex:
            logging.exception(ex)
            raise ex  # noqa: TRY201

        return result

    def get_validators(self) -> list[t.Callable]:
        return []

    def validate(self) -> None:
        validators = self.get_validators()
        for validator in validators:
            validator()

    @abstractmethod
    def act(self) -> t.Any:
        raise NotImplementedError("Please implement in the service class")
