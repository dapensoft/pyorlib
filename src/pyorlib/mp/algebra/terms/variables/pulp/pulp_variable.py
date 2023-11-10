from math import inf
from typing import Any

from pulp import LpVariable, LpProblem, LpBinary, LpInteger, LpContinuous

from src.pyorlib.mp.algebra.terms.variables.variable import Variable
from src.pyorlib.mp.enums import ValueType
from src.pyorlib.mp.exceptions import PuLPException


class PuLPVariable(Variable):
    """
    Represents a PuLP variable in an optimization model.

    The `PuLPVariable` class is a concrete implementation of the abstract `Variable` class.
    It represents a variable that is compatible with the PuLP solver.
    """

    # Strict class attributes.
    __slots__ = ["_pulp_var"]

    @property
    def name(self) -> str:
        return self._pulp_var.name

    @property
    def lower_bound(self) -> float:
        lb = self._pulp_var.lowBound
        return lb if lb is not None else -inf

    @property
    def upper_bound(self) -> float:
        ub = self._pulp_var.upBound
        return ub if ub is not None else inf

    @property
    def value(self) -> float:
        val = self._pulp_var.value()
        return val if val else -0.0

    @property
    def raw(self) -> Any:
        return self._pulp_var

    def __init__(
            self,
            name: str,
            solver: LpProblem,
            value_type: ValueType,
            lower_bound: float | None = None,
            upper_bound: float | None = None
    ):
        """
        Initializes a new `PuLPVariable` object with the specified attributes and creates a corresponding PuLP
        variable in the PuLP solver.
        :param name: The name of the variable.
        :param solver: A reference to the PuLP solver.
        :param value_type: An enumeration representing the type of the variable's value.
        :param lower_bound: The lower bound of the variable, or None. Default is 0.
        :param upper_bound: The upper bound of the variable, or None, to use the default. Default is infinity.
        """
        # Calls the super init method with the value type.
        super().__init__(value_type=value_type)

        # Checks for none values
        if solver is None:
            raise PuLPException("The solver reference cannot be None.")
        if not name:
            raise PuLPException("PuLP terms must have a name.")

        # Creates the PuLP variable according to the value type
        pulp_var: LpVariable

        if self.value_type == ValueType.BINARY:
            pulp_var = LpVariable(
                name=name,
                cat=LpBinary,
                lowBound=0,
                upBound=1
            )
        elif self.value_type == ValueType.INTEGER:
            pulp_var = LpVariable(
                name=name,
                cat=LpInteger,
                lowBound=lower_bound if lower_bound else 0.0,
                upBound=upper_bound
            )
        elif self.value_type == ValueType.CONTINUOUS:
            pulp_var = LpVariable(
                name=name,
                cat=LpContinuous,
                lowBound=lower_bound if lower_bound else 0.0,
                upBound=upper_bound
            )
        else:
            raise PuLPException("Invalid term ValueType.")

        # Instance attributes
        self._pulp_var: LpVariable = pulp_var
        """ A LpVariable object representing the variable in the PuLP solver. """

        # Checks for none values
        if self._pulp_var is None:
            raise PuLPException("Failed to create the PuLP variable.")

        # Apply validations.
        self.validate()
