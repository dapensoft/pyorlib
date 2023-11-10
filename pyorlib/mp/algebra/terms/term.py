from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from pyorlib.core.constants import StdOutColors
from pyorlib.mp.enums import TermType, ValueType
from pyorlib.mp.exceptions import TermException
from pyorlib.mp.algebra.element import Element
from pyorlib.mp.algebra.expressions.expression import Expression


@dataclass
class Term(Element, ABC):
    """
    A base class representing a term in an optimization model.

    The `Term` class serves as a base class for representing terms in an optimization model. It is designed to
    be inherited by subclasses that represent specific types of terms. The `Term` class itself is an abstract
    base class (ABC) that defines the common behavior and interface for all terms.
    """

    __slots__ = ["_term_type", "_value_type"]

    @property
    def term_type(self) -> TermType:
        """
        Retrieves the type of the term.
        :return: A TermType enumeration.
        """
        return self._term_type

    @property
    def value_type(self) -> ValueType:
        """
        Retrieves the type of the term's value.
        :return: A ValueType enumeration
        """
        return self._value_type

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Retrieves the name of the term.
        :return: A string with name of the term.
        """
        pass

    @property
    @abstractmethod
    def lower_bound(self) -> float:
        """
        Retrieves the lower bound of the term's value.
            For variable terms, the lower bound denotes the minimum value that the term can assume.
            For constant terms, the lower bound is equivalent to its value.
        :return: A float representing the lower bound of the term's value. If the upper bound is negative infinity,
            the method returns `-inf` from the math module.
        """
        pass

    @property
    @abstractmethod
    def upper_bound(self) -> float:
        """
        Retrieves the upper bound of the term's value.
            For variable terms, the upper bound denotes the maximum value that the term can assume.
            For constant terms, the upper bound is equivalent to its value.
        :return: A float representing the upper bound of the term's value. If the upper bound is infinity,
            the method returns `inf` from the math module.
        """
        pass

    @property
    @abstractmethod
    def value(self) -> float:
        """
        Retrieves the value of the term.
            For variable terms, the value corresponds to the current value of the term.
            If the term has not been solved yet, the value is `-0.0`.
            For constant terms, the value remains the constant value.
        :return: A float representing the value of the term.
        """
        pass

    @property
    def is_variable(self) -> bool:
        """
        Determines whether the term is a variable or not.
        :return: `True` if the term is a variable, `False` otherwise.
        """
        return self._term_type == TermType.VARIABLE

    @property
    def is_constant(self) -> bool:
        """
        Determines whether the term is a constant or not.
        :return: `True` if the term is a constant, `False` otherwise.
        """
        return self._term_type == TermType.CONSTANT

    def __init__(self, term_type: TermType, value_type: ValueType):
        """
        Initializes a new Term object.
        :param term_type: An enumeration representing the type of the term.
        :param value_type: An enumeration representing the type of the term's value.
        """
        if not term_type:
            raise TermException("Invalid term type.")
        if not value_type:
            raise TermException("Invalid term value type.")

        # Instance attributes
        self._term_type: TermType = term_type
        """ An enumeration representing the type of the term. """

        self._value_type: ValueType = value_type
        """ An enumeration representing the type of the term's value. """

    @abstractmethod
    def validate(self) -> None:
        """
        Validates the term to ensure its correct definition.

        This method checks the validity and consistency of the term's attributes. It verifies that the term is
        correctly defined and ready to be used in an optimization problem. If any inconsistencies or invalid
        attributes are found, an `Exception` may be raised to indicate the issue.
        :return: None
        """
        pass

    def _build_expression(self, expression: Any) -> Element:
        return Expression(expression=expression)

    def get_pretty_string(self, float_precision: int = 6) -> str:
        """
        Returns a formatted string representation of the term.
        :param float_precision: It represents the number of digits used in printing the solution and objective.
        :return: A formatted string representing the term.
        """
        default, debug = StdOutColors.DEFAULT, StdOutColors.PURPLE
        return "".join([
            f"Name: {debug}{self.name}{default} | ",
            f"Type: {debug}{self.term_type.name.capitalize()}{default} | ",
            f"Value type: {debug}{self.value_type.name.capitalize()}{default} | ",
            f"lb:{debug} ", '{0:.{prec}g} '.format(self.lower_bound, prec=float_precision), f"{default}| ",
            f"ub:{debug} ", '{0:.{prec}g} '.format(self.upper_bound, prec=float_precision), f"{default}| ",
            f"val:{debug} ", '{0:.{prec}g} '.format(self.value, prec=float_precision), f"{default}",
        ])

    def __str__(self):
        return "".join([
            f"Name: {self.name} | ",
            f"Type: {self.term_type.name} | ",
            f"Value type: {self.value_type.name} | ",
            f"lb: {self.lower_bound} | ",
            f"ub: {self.upper_bound} | ",
            f"val: {self.value}",
        ])

    def __iadd__(self, other) -> Element:
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw + other.raw)
        else:
            return self._build_expression(expression=self.raw + other)

    def __isub__(self, other) -> Element:
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw - other.raw)
        else:
            return self._build_expression(expression=self.raw - other)

    def __imul__(self, other) -> Element:
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw * other.raw)
        else:
            return self._build_expression(expression=self.raw * other)

    def __itruediv__(self, other) -> Element:
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw / other.raw)
        else:
            return self._build_expression(expression=self.raw / other)

    def __ifloordiv__(self, other) -> Element:
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw // other.raw)
        else:
            return self._build_expression(expression=self.raw // other)

    def __imod__(self, other) -> Element:
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw % other.raw)
        else:
            return self._build_expression(expression=self.raw % other)

    def __ipow__(self, other) -> Element:
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw ** other.raw)
        else:
            return self._build_expression(expression=self.raw ** other)
