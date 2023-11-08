from typing import List

from ortools.linear_solver.pywraplp import Solver, MPSolverParameters

from pyorlib.core.loggers import StdOutLogger
from pyorlib.mp.common.enums import SolutionStatus, ValueType, OptimizationType
from pyorlib.mp.common.exceptions import ORToolsException
from pyorlib.mp.engines.engine import Engine
from pyorlib.mp.math import Element
from pyorlib.mp.math.expressions import Expression
from pyorlib.mp.math.terms.variables import Variable
from pyorlib.mp.math.terms.variables.ortools import ORToolsVariable


class ORToolsEngine(Engine):
    """
    This class provides a high-level interface for solving
    optimization problems using the OR-Tools package.
    """

    @property
    def name(self) -> str:
        return "OR-Tools Engine"

    @property
    def constraints(self) -> List[Element]:
        return [Expression(expression=constraint) for constraint in self._solver.constraints()]

    @property
    def objective_value(self) -> float | None:
        if self.solution_status in [SolutionStatus.OPTIMAL, SolutionStatus.FEASIBLE]:
            return self._solver.Objective().Value()
        return None

    @property
    def objective_expr(self) -> Element | None:
        objective = self._solver.Objective()
        return Expression(expression=objective) if objective is not None else None

    @property
    def solution_status(self) -> SolutionStatus:
        if self._status == Solver.NOT_SOLVED:
            return SolutionStatus.NOT_SOLVED
        elif self._status == Solver.OPTIMAL:
            return SolutionStatus.OPTIMAL
        elif self._status == Solver.FEASIBLE:
            return SolutionStatus.FEASIBLE
        elif self._status == Solver.INFEASIBLE:
            return SolutionStatus.INFEASIBLE
        elif self._status in [Solver.UNBOUNDED, Solver.MODEL_INVALID, Solver.ABNORMAL]:
            return SolutionStatus.ERROR
        else:
            StdOutLogger.error(action="Solution status: ", msg=f"{self._status}")
            raise ORToolsException('Invalid OR-Tools status code.')

    def __init__(
            self,
            solver: Solver | None = None,
            solver_params: MPSolverParameters | None = None,
    ):
        """
        Initializes a new instance of the ORToolsSolver class.
        :param solver: Specifies a ORTools solver (ortools.linear_solver.pywraplp) to be used by the engine. Default is None (instantiates a default solver with SCIP).
        """

        # Instance attributes
        self._solver: Solver = solver if solver else Solver.CreateSolver(solver_id='SCIP')
        """ A reference to the OR-Tools solver. """

        # Set or tools configuration
        self._solver_params: MPSolverParameters = solver_params if solver_params else MPSolverParameters()

        self._status: int = 6
        """ Represents the state of the solution. """

        if self._solver is None:
            ORToolsException("Failed to create the OR-Tools solver.")

    def add_variable(
            self,
            name: str,
            value_type: ValueType,
            lower_bound: float | None = None,
            upper_bound: float | None = None
    ) -> Variable:
        return ORToolsVariable(
            name=name,
            solver=self._solver,
            value_type=value_type,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            solution_status=lambda: self.solution_status,
        )

    def add_constraint(self, expression: Element) -> Element:
        self._solver.Add(constraint=expression.raw)
        return expression

    def set_objective(self, opt_type: OptimizationType, expression: Element) -> Element:
        if opt_type == OptimizationType.MINIMIZE:
            self._solver.Minimize(expr=expression.raw)
        elif opt_type == OptimizationType.MAXIMIZE:
            self._solver.Maximize(expr=expression.raw)
        else:
            raise ORToolsException('Invalid optimization type.')
        return expression

    def solve(self) -> None:
        self._status = self._solver.Solve(self._solver_params)

    def clear(self) -> None:
        self._solver.Clear()
