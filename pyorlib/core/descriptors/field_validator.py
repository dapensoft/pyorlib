from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class FieldValidator(Generic[T], ABC):
    """
    A generic abstract base class that represents a validator for a
    field in a data class that has a specific type T
    """

    __slots__ = ["_private_name", "_public_name", "_default"]

    def __init__(self, default: T | None = None):
        """
        Initializes a FieldValidator object.
        :param default: The default value for the field.
        """
        self._default = default

    def __set_name__(self, owner, name) -> None:
        self._private_name = '_' + name
        self._public_name = name

    def __get__(self, obj, objtype=None) -> T:
        return getattr(obj, self._private_name)

    def __set__(self, obj, value: T) -> None:
        val = value if value else self._default
        self.validate(val)
        setattr(obj, self._private_name, val)

    @abstractmethod
    def validate(self, value: T | None) -> None:
        """
        Validates a value for a field in a data class that has a specific type T.
        :param value: The value to be validated.
        :return: None
        """
        pass
