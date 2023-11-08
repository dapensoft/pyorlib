from typing import List, Any

from pulp import LpProblem, LpMaximize, LpMinimize, value, LpSolverDefault

from pyorlib.core.logger import StdOutLogger
from pyorlib.mp.common.enums import SolutionStatus, ValueType, OptimizationType
from pyorlib.mp.common.exceptions import PuLPException
from pyorlib.mp.engines.engine import Engine
from pyorlib.mp.math import Element
from pyorlib.mp.math.expressions import Expression
from pyorlib.mp.math.terms.variables import Variable
from pyorlib.mp.math.terms.variables.pulp import PuLPVariable


class PuLPEngine(Engine):
    """
    This class provides a high-level interface for solving mathematical
    optimization problems using the PuLP solver.
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
            return value(self._solver.objective)
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
            raise PuLPException('Invalid PuLP status code.')

    def __init__(self, solver: LpProblem | None = None):
        """
        Initializes a new instance of the PulpSolver class.
        :param solver: Specifies a PuLP solver (LpProblem) to be used by the engine. Default is None (instantiates a default solver).
        """

        # Instance attributes
        self._solver: LpProblem = solver if solver else LpProblem()
        """ A reference to the PuLP solver. """

        if self._solver is None:
            PuLPException("Failed to create the PuLP solver.")

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
        self._solver += expression.expr
        return expression

    def set_objective(self, opt_type: OptimizationType, expression: Element) -> Element:
        if opt_type == OptimizationType.MINIMIZE:
            self._solver.sense = LpMinimize
        elif opt_type == OptimizationType.MAXIMIZE:
            self._solver.sense = LpMaximize
        else:
            raise PuLPException('Invalid optimization type.')
        self._solver.setObjective(expression.expr)
        self._objective = expression.expr
        return expression

    def solve(self) -> None:
        solve_param = LpSolverDefault.msg = False
        self._status = self._solver.solve(solve_param)

    def clear(self) -> None:
        raise PuLPException('This method is not implemented.')
