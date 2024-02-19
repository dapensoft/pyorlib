from abc import ABC, abstractmethod
from typing import Generic, TypeVar, cast

T = TypeVar("T")
"""The type of the field value."""


class FieldValidator(Generic[T], ABC):
    """
    A generic abstract base class that represents a validator for a field in a data class.

    This class provides a foundation for creating custom field validators that can be used as descriptors in Python
    classes. Field validators are responsible for validating and processing values assigned to specific attributes.
    """

    __slots__ = ["_private_name", "_public_name", "_default"]

    def __init__(self, default: T | None = None):
        """
        Initializes a FieldValidator instance.
        :param default: The default value for the field. If not provided, defaults to None.
        """
        self._default = default

    def __set_name__(self, owner: type[object], name: str) -> None:
        """
        Sets the name of the field during class attribute assignment.
        :param owner: The owner class of the attribute.
        :param name: The name of the attribute.
        :return: None.
        """
        self._private_name: str = "_" + name
        self._public_name: str = name

    def __get__(self, obj: object, objtype: type[object] | None = None) -> T:
        """
        Retrieves the value of the field.
        :param obj: The instance of the object.
        :param objtype: The type of the object.
        :return: The value of the field.
        """
        return cast(T, getattr(obj, self._private_name))

    def __set__(self, obj: object, value: T) -> None:
        """
        Sets the value of the field.
        :param obj: The instance of the object.
        :param value: The value to be set for the field.
        :return: None.
        """
        val: T | None = value if value else self._default
        self.validate(val)
        setattr(obj, self._private_name, val)

    @abstractmethod
    def validate(self, value: T | None) -> None:
        """
        Validates the value of the field.
        :param value: The value to be validated.
        :return: None.
        """
        pass
