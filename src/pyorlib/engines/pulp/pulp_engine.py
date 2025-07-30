from math import inf
from typing import List, Any

from ..engine import Engine
from ...algebra import Element
from ...algebra.expressions import Expression
from ...algebra.terms.variables import Variable
from ...core.loggers import StdOutLogger
from ...enums import SolutionStatus, ValueType, OptimizationType
from ...exceptions import PuLPException

try:  # pragma: no cover
    from pulp import (
        LpProblem,
        LpMaximize,
        LpMinimize,
        value,
        LpSolverDefault,
        LpVariable,
        LpBinary,
        LpInteger,
        LpContinuous,
    )
except ImportError:  # pragma: no cover
    raise PuLPException("Optional dependency 'PuLP' not found.\nPlease install it using 'pip install pyorlib[pulp]'.")


class PuLPEngine(Engine):
    """
    Concrete engine implementation using PuLP.

    This class provides a PuLP-based implementation of the abstract Engine interface for formulating
    and solving linear and integer optimization models.
    """

    class _Variable(Variable):
        """
        Represents a PuLP variable in an optimization model.

        The `PuLPVariable` class is a concrete implementation of the abstract `Variable` class.
        It represents a variable that is compatible with the PuLP solver.
        """

        # Strict class attributes.
        __slots__ = ["_pulp_var"]

        @property
        def name(self) -> str:
            return str(self._pulp_var.name)

        @property
        def lower_bound(self) -> float:
            lb = self._pulp_var.lowBound
            return float(lb) if lb is not None else -inf

        @property
        def upper_bound(self) -> float:
            ub = self._pulp_var.upBound
            return float(ub) if ub is not None else inf

        @property
        def value(self) -> float:
            val = self._pulp_var.value()
            return float(val) if val else -0.0

        @property
        def raw(self) -> Any:
            return self._pulp_var

        def __init__(
            self,
            name: str,
            solver: LpProblem,
            value_type: ValueType,
            lower_bound: float = 0,
            upper_bound: float = inf,
        ):
            """
            Initializes a new `PuLPVariable` object with the specified attributes and creates a corresponding PuLP
            variable in the PuLP solver.
            :param name: The name of the variable.
            :param solver: A reference to the PuLP solver.
            :param value_type: An enumeration representing the type of the variable's value.
            :param lower_bound: The lower bound of the variable. Default is 0.
            :param upper_bound: The upper bound of the variable. Default is infinity.
            """
            # Calls the super init method and its validations
            super().__init__(name=name, value_type=value_type, lower_bound=lower_bound, upper_bound=upper_bound)

            # Applies new validations
            if solver is None:
                raise PuLPException("The 'solver' argument cannot be None.")

            # Creates the PuLP variable according to the value type
            pulp_var: LpVariable | None

            if self.value_type == ValueType.BINARY:
                pulp_var = LpVariable(name=name, cat=LpBinary, lowBound=0, upBound=1)
            elif self.value_type == ValueType.INTEGER:
                pulp_var = LpVariable(
                    name=name,
                    cat=LpInteger,
                    lowBound=lower_bound if lower_bound > -inf else None,
                    upBound=upper_bound if upper_bound < inf else None,
                )
            elif self.value_type == ValueType.CONTINUOUS:
                pulp_var = LpVariable(
                    name=name,
                    cat=LpContinuous,
                    lowBound=lower_bound if lower_bound > -inf else None,
                    upBound=upper_bound if upper_bound < inf else None,
                )
            else:
                raise PuLPException("Unknown ValueType.")

            # Applies new validations
            if pulp_var is None:  # pragma: no cover
                raise PuLPException("Failed to create the PuLP variable.")

            # Instance attributes
            self._pulp_var: LpVariable = pulp_var
            """ A LpVariable object representing the variable in the PuLP solver. """

    @property
    def name(self) -> str:  # pragma: no cover
        return "PuLP Engine"

    @property
    def constraints(self) -> List[Element]:
        return [Expression(expression=constraint) for constraint in self._solver.constraints.values()]

    @property
    def objective_value(self) -> float | None:
        if self.solution_status in [SolutionStatus.OPTIMAL, SolutionStatus.FEASIBLE]:
            return float(value(self._solver.objective))
        return None

    @property
    def objective_expr(self) -> Element | None:
        return Expression(expression=self._objective) if self._objective is not None else None

    @property
    def solution_status(self) -> SolutionStatus:  # pragma: no cover
        if self._status == 0:
            return SolutionStatus.NOT_SOLVED
        elif self._status == 1:
            return SolutionStatus.OPTIMAL
        elif self._status == -1:
            return SolutionStatus.INFEASIBLE
        elif self._status in [-2, -3]:
            return SolutionStatus.ERROR
        else:
            StdOutLogger.error(action="Solution status: ", msg=f"{self._status}")
            raise PuLPException("Unhandled PuLP status code.")

    def __init__(self, solver: LpProblem | None = None):
        """
        Initializes the PuLPEngine instance.

        The solver parameter enables the user to pass a pre-configured PuLP solver with custom parameters
        instead of using the default solver. This allows greater flexibility in specifying solver options.
        :param solver: A pre-configured PuLP LpProblem
            object to use as the solver. This allows custom configuration
            of the solver before passing to the engine. If None, a default
            solver will be instantiated with default settings.
            Defaults to None.
        """

        # Instance attributes
        self._solver: LpProblem = solver if solver else LpProblem()
        """ A reference to the PuLP solver. """

        if self._solver is None or not isinstance(self._solver, LpProblem):
            raise PuLPException("The PuLP solver cannot be None.")

        self._objective: Any = None
        """ An object representing the optimization function of the problem. """

        self._status: int = 0
        """ Represents the state of the solution. """

    def add_variable(
        self,
        name: str,
        value_type: ValueType,
        lower_bound: float = 0,
        upper_bound: float = inf,
    ) -> Variable:
        return PuLPEngine._Variable(
            name=name,
            solver=self._solver,
            value_type=value_type,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )

    def add_constraint(self, expression: Element) -> Element:
        self._solver += expression.raw
        return expression

    def set_objective(self, opt_type: OptimizationType, expression: Element) -> Element:
        if opt_type == OptimizationType.MINIMIZE:
            self._solver.sense = LpMinimize
        elif opt_type == OptimizationType.MAXIMIZE:
            self._solver.sense = LpMaximize
        else:
            raise PuLPException("Optimization type not supported.")
        self._solver.setObjective(expression.raw)
        self._objective = expression.raw
        return expression

    def solve(self) -> None:
        solve_param = LpSolverDefault.msg = False
        self._status = self._solver.solve(solve_param)
