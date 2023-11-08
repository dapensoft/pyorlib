from typing import Any, Callable

from ortools.linear_solver.pywraplp import Solver as ORToolsSolver, inf as ORToolsInf, Variable as ORToolsVar

from pyorlib.mp.common.enums import SolutionStatus, ValueType
from pyorlib.mp.common.exceptions import ORToolsException
from pyorlib.mp.math.terms.variables.variable import Variable


class ORToolsVariable(Variable):
    """ Represents a variable in a mathematical expression that can be used with the OR-Tools solver. """

    __slots__ = ["_ortools_var", "_solution_status"]

    @property
    def name(self) -> str:
        return self._ortools_var.name()

    @property
    def lower_bound(self) -> float:
        return self._ortools_var.lb()

    @property
    def upper_bound(self) -> float:
        return self._ortools_var.ub()

    @property
    def value(self) -> float:
        if self._solution_status() in [SolutionStatus.OPTIMAL, SolutionStatus.FEASIBLE]:
            return round(self._ortools_var.solution_value(), 6)
        else:
            return -0.0

    @property
    def raw(self) -> Any:
        return self._ortools_var

    def __init__(
            self,
            name: str,
            solver: ORToolsSolver,
            value_type: ValueType,
            solution_status: Callable[[], SolutionStatus],
            lower_bound: float | None = None,
            upper_bound: float | None = None,
    ):
        """
        Initializes a new ORToolsVariable object with the specified attributes and creates
        a corresponding OR-Tools variable.
        :param name: The name of the variable.
        :param solver: A reference to the OR-Tools solver.
        :param value_type: An enumeration representing the type of the variable's value.
        :param lower_bound: The lower bound of the variable, or None. The default is 0.
        :param upper_bound: The upper bound of the variable, or None, to use the default. The default is infinity.
        """
        # Calls the super init method with the value type.
        super().__init__(value_type=value_type)

        if solver is None:
            raise ORToolsException("The solver value cannot be none.")
        if not name:
            raise ORToolsException("OR-Tool terms must have a name.")

        # Creates the OR-Tools variable according to the value type
        ortools_var: ORToolsVar

        if self.value_type == ValueType.BINARY:
            ortools_var = solver.BoolVar(
                name=name
            )
        elif self.value_type == ValueType.INTEGER:
            ortools_var = solver.IntVar(
                name=name,
                lb=lower_bound if lower_bound is not None else 0,
                ub=upper_bound if upper_bound is not None else ORToolsInf,
            )
        elif self.value_type == ValueType.CONTINUOUS:
            ortools_var = solver.NumVar(
                name=name,
                lb=lower_bound if lower_bound is not None else 0,
                ub=upper_bound if upper_bound is not None else ORToolsInf,
            )
        else:
            raise ORToolsException("Invalid term value type.")

        # Instance attributes
        self._solution_status: Callable[[], SolutionStatus] = solution_status
        """ A callable to check the current status of the solution. """

        self._ortools_var: ORToolsVar = ortools_var
        """ A pywraplp.Variable object representing the variable in the OR-Tools solver. """

        if self._solution_status is None:
            raise ORToolsException("The solution status callable cannot be none.")

        if self._ortools_var is None:
            raise ORToolsException("Failed to create the OR-Tools variable.")

        # Apply validations.
        self.validate()
