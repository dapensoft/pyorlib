from abc import ABC
from math import inf

from src.pyorlib.mp.algebra.terms.term import Term
from src.pyorlib.mp.enums import ValueType, TermType
from src.pyorlib.mp.exceptions import TermException


class Variable(Term, ABC):
    """
    Represents a base class for variable terms in an optimization model.

    The `Variable` class is a subclass of `Term` and serves as a foundation for representing variable terms in
    optimization models. It is designed to be inherited by subclasses that represent specific types of
    variables. As an abstract base class (ABC), `Variable` defines the common behavior and interface
    for all variable terms.
    """

    def __init__(self, value_type: ValueType):
        """
        Initializes a new `Variable` object with the specified attributes.
        :param value_type: A `ValueType` enumeration representing the type of the variable.
        """
        # Calls the base init with the term type as Variable.
        super().__init__(term_type=TermType.VARIABLE, value_type=value_type)

    def validate(self) -> None:
        # Validates the lower and upper bounds
        if not self.name:
            raise TermException("Variable terms must have a name.")
        if self.lower_bound >= inf:
            raise TermException("Variable terms lower bounds cannot be +infinity.")
        if self.upper_bound <= -inf:
            raise TermException("Variable terms upper bounds cannot be -infinity.")
        if self.lower_bound > self.upper_bound:
            raise TermException("The lower bound of a variable cannot be greater than the upper bound.")
        if self.lower_bound is None or self.upper_bound is None:
            raise TermException("Variable terms must have lower and upper bounds.")
        if self.value_type == ValueType.BINARY and (self.lower_bound != 0 or self.upper_bound != 1):
            raise TermException("Invalid bounds for a binary variable.")
        if self.value_type == ValueType.INTEGER and \
                not self.lower_bound == -inf and not float(self.lower_bound).is_integer():
            raise TermException("Invalid lower bound for an integer variable term.")
        if self.value_type == ValueType.INTEGER and \
                not self.upper_bound == inf and not float(self.upper_bound).is_integer():
            raise TermException("Invalid upper bound for an integer variable term.")
