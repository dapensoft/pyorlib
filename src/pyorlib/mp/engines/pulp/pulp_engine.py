from typing import List, Any

from ..engine import Engine
from ...algebra import Element
from ...algebra.expressions import Expression
from ...algebra.terms.variables import Variable
from ...algebra.terms.variables.pulp import PuLPVariable
from ...enums import SolutionStatus, ValueType, OptimizationType
from ...exceptions import PuLPException
from ....core.loggers import StdOutLogger

try:  # pragma: no cover
    from pulp import LpProblem, LpMaximize, LpMinimize, value, LpSolverDefault
except ImportError:  # pragma: no cover
    raise PuLPException(
        "Optional dependency 'PuLP' not found."
        "\nPlease install it using 'pip install pyorlib[pulp]'."
    )


class PuLPEngine(Engine):
    """
    Concrete engine implementation using PuLP.

    This class provides a PuLP-based implementation of the abstract Engine interface for formulating
    and solving linear and integer optimization models.
    """

    @property
    def name(self) -> str:
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
    def solution_status(self) -> SolutionStatus:
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
            raise PuLPException('Unhandled PuLP status code.')

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

        if self._solver is None:
            raise PuLPException("The PuLP solver cannot be None.")

        self._objective: Any = None
        """ An object representing the optimization function of the problem. """

        self._status: int = 0
        """ Represents the state of the solution. """

    def add_variable(
            self,
            name: str,
            value_type: ValueType,
            lower_bound: float | None = None,
            upper_bound: float | None = None
    ) -> Variable:
        return PuLPVariable(
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
            raise PuLPException('Optimization type not supported.')
        self._solver.setObjective(expression.raw)
        self._objective = expression.raw
        return expression

    def solve(self) -> None:
        solve_param = LpSolverDefault.msg = False
        self._status = self._solver.solve(solve_param)

    def clear(self) -> None:
        raise PuLPException('This method is not implemented.')
