from math import inf
from typing import Any

from ..variable import Variable
from .....enums import ValueType
from .....exceptions import CplexException

try:  # pragma: no cover
    import docplex.mp.model as cpx
    from docplex.mp.dvar import Var
    from docplex.mp.utils import DOcplexException
except ImportError:  # pragma: no cover
    raise CplexException(
        "Optional dependency 'CPLEX' not found."
        "\nPlease install it using 'pip install pyorlib[cplex]'."
    )


class CplexVariable(Variable):
    """
    Represents a CPLEX variable in an optimization model.

    The `CplexVariable` class is a concrete implementation of the abstract `Variable` class.
    It represents a variable that is compatible with the CPLEX solver.
    """

    # Strict class attributes.
    __slots__ = ["_cplex_var"]

    @property
    def name(self) -> str:
        return self._cplex_var.name

    @property
    def lower_bound(self) -> float:
        lb = self._cplex_var.lb
        return -inf if lb <= -1e20 else lb

    @property
    def upper_bound(self) -> float:
        ub = self._cplex_var.ub
        return inf if ub >= 1e20 else ub

    @property
    def value(self) -> float:
        try:
            return self._cplex_var.solution_value
        except DOcplexException:
            return -0.0

    @property
    def raw(self) -> Any:
        return self._cplex_var

    def __init__(
            self,
            name: str,
            solver: cpx.Model,
            value_type: ValueType,
            lower_bound: float | None = None,
            upper_bound: float | None = None
    ):
        """
        Initializes a new `CplexVariable` object with the specified attributes and creates a corresponding CPLEX
        variable in the specified CPLEX solver.
        :param name: The name of the variable.
        :param solver: A reference to the CPLEX solver.
        :param value_type: An enumeration representing the type of the variable's value.
        :param lower_bound: The lower bound of the variable, or None. Default is 0.
        :param upper_bound: The upper bound of the variable, or None, to use the default. Default is infinity.
        """
        # Calls the super init method with the value type.
        super().__init__(value_type=value_type)

        if solver is None:
            raise CplexException("The solver reference cannot be None.")
        if not name:
            raise CplexException("CPLEX terms must have a name.")

        # Creates the CPLEX variable according to the value type
        cplex_var: Var

        if self.value_type == ValueType.BINARY:
            cplex_var = solver.binary_var(name=name)
        elif self.value_type == ValueType.INTEGER:
            cplex_var = solver.integer_var(name=name, lb=lower_bound, ub=upper_bound)
        elif self.value_type == ValueType.CONTINUOUS:
            cplex_var = solver.continuous_var(name=name, lb=lower_bound, ub=upper_bound)
        else:
            raise CplexException("Invalid term ValueType.")

        # Instance attributes
        self._cplex_var: Var = cplex_var
        """ A Cplex.Var object representing the variable in the CPLEX solver. """

        if self._cplex_var is None:
            raise CplexException("Failed to create the CPLEX variable.")

        # Apply validations.
        self.validate()
