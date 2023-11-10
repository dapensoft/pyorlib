from math import inf
from typing import Any

from pyorlib.mp.enums import ValueType, TermType
from pyorlib.mp.exceptions import TermException
from pyorlib.mp.validators import ValueTypeValidator
from pyorlib.mp.algebra.terms.term import Term


class Constant(Term):
    """
    Represents a constant value in an optimization model.

    The `Constant` class is a subclass of `Term` and represents a fixed value that remains constant
    throughout the optimization process. It is typically used to represent known values or
    parameters in an optimization model.
    """

    __slots__ = ["_name", "_value"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def lower_bound(self) -> float:
        return self._value

    @property
    def upper_bound(self) -> float:
        return self._value

    @property
    def value(self) -> float:
        return self._value

    @property
    def raw(self) -> Any:
        return self.value

    def __init__(self, name: str, value_type: ValueType, value: float):
        """
        Initializes a new instance of the Constant class.
        :param name: A string representing the name of the constant.
        :param value_type: A ValueType enumeration representing the type of value the constant can assume.
        :param value: A float representing the value of the constant.
        """
        # Calls the super init method.
        super().__init__(term_type=TermType.CONSTANT, value_type=value_type)

        self._name: str = name
        """ The name of the constant. """

        self._value: float = value
        """ The internal value of the constant. """

        # Applies validation
        self.validate()

    def validate(self) -> None:
        # Validates the value
        if not self.name:
            raise TermException("Constant terms must have a name.")
        if self.value is None:
            raise TermException("Constant terms must have a value.")
        if self.value >= inf or self.value <= -inf:
            raise TermException("Constant terms value cannot be greater than or equal to [+/-]infinity.")
        if self.lower_bound != self.value or self.upper_bound != self.value:
            raise TermException("Invalid bounds for a constant term.")
        if self.value_type == ValueType.BINARY and not ValueTypeValidator.is_binary(num=self.value):
            raise TermException("The value of a binary constant must be 0 or 1.")
        if self.value_type == ValueType.INTEGER and not ValueTypeValidator.is_integer(num=self.value):
            raise TermException("The value of an integer constant must be a valid integer.")
