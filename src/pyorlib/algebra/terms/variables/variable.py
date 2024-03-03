from abc import ABC
from math import inf

from ..term import Term
from ....core.constants import StdOutColors
from ....enums import ValueType, TermType
from ....exceptions import TermException


class Variable(Term, ABC):
    """
    Represents a base class for variable terms in an optimization model.

    The `Variable` class is a subclass of `Term` and serves as a foundation for representing variable terms in
    optimization models. It is designed to be inherited by subclasses that represent specific types of
    variables. As an abstract base class (ABC), `Variable` defines the common behavior and interface
    for all variable terms.
    """

    def __init__(self, name: str, value_type: ValueType, lower_bound: float = 0, upper_bound: float = inf):
        """
        Initializes a new `Variable` object with the specified attributes.
        :param name: The name of the variable.
        :param value_type: An enumeration representing the type of the variable's value.
        :param lower_bound: The lower bound of the variable. Default is 0.
        :param upper_bound: The upper bound of the variable. Default is infinity.
        """
        # Calls the base init with the term type as Variable.
        super().__init__(term_type=TermType.VARIABLE, value_type=value_type)

        # Applies validations
        if not name:
            raise TermException("Variable terms must have a name.")
        if lower_bound is None or upper_bound is None:
            raise TermException("Variable terms must have lower and upper bounds.")
        if lower_bound >= inf:
            raise TermException("Variable terms lower bounds cannot be +infinity.")
        if upper_bound <= -inf:
            raise TermException("Variable terms upper bounds cannot be -infinity.")
        if lower_bound > upper_bound:
            raise TermException("The lower bound of a variable cannot be greater than the upper bound.")
        if value_type == ValueType.BINARY and (lower_bound != 0 or (upper_bound != 1 and upper_bound != inf)):
            raise TermException("Invalid bounds for a binary variable.")
        if value_type == ValueType.INTEGER and not lower_bound == -inf and not float(lower_bound).is_integer():
            raise TermException("Invalid lower bound for an integer variable term.")
        if value_type == ValueType.INTEGER and not upper_bound == inf and not float(upper_bound).is_integer():
            raise TermException("Invalid upper bound for an integer variable term.")

    def get_pretty_string(self, float_precision: int = 6) -> str:  # pragma: no cover
        default, debug = StdOutColors.DEFAULT, StdOutColors.PURPLE
        return "".join(
            [
                f"Name: {debug}{self.name}{default} | ",
                f"Type: {debug}{self.term_type.name.capitalize()}{default} | ",
                f"Value type: {debug}{self.value_type.name.capitalize()}{default} | ",
                f"Lb:{debug} ",
                "{0:.{prec}g} ".format(self.lower_bound, prec=float_precision),
                f"{default}| Ub:{debug} ",
                "{0:.{prec}g} ".format(self.upper_bound, prec=float_precision),
                f"{default}| Val:{debug} ",
                "{0:.{prec}g} ".format(self.value, prec=float_precision),
                f"{'(N/A) ' if self.value == -0.0 else ''}{default}",
            ]
        )
