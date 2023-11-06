from typing import List

from ortools.linear_solver.pywraplp import Solver, MPSolverParameters

from pyorlib.core.logger import StdOutLogger
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
            solver_backend: str = "SCIP",
            time_limit: float | None = None,
            mip_gap: float | None = None,
            num_threads: int | None = None,
            presolve: int | None = None,
    ):
        """
        Initializes a new instance of the ORToolsSolver class.

        :param solver_backend: It will accept both string names of the OptimizationProblemType enum, and a short version (i.e. "SCIP_MIXED_INTEGER_PROGRAMMING" or "SCIP").
        :param time_limit: The time limit for the solver in milliseconds. Default is None (no time limit).
        :param mip_gap: Limit for relative MIP gap. Default is None (no time limit).
        :param num_threads: The number of solver threads to use. Default is None (use solver default).
        :param presolve: Controls the presolve level. Default is None (use solver default).
        """

        # Instance attributes
        self._solver: Solver = Solver.CreateSolver(solver_id=solver_backend)
        """ A reference to the OR-Tools solver. """

        self._status: int = 6
        """ Represents the state of the solution. """

        if self._solver is None:
            ORToolsException("Failed to create the OR-Tools solver.")

        # Set or tools configuration
        self._solver_params: MPSolverParameters = MPSolverParameters()

        if time_limit is not None:
            self._solver.set_time_limit(time_limit_milliseconds=time_limit)
        if mip_gap is not None:
            self._solver_params.SetDoubleParam(self._solver_params.RELATIVE_MIP_GAP, mip_gap)
        if num_threads is not None:
            self._solver.SetNumThreads(num_theads=num_threads)
        if presolve is not None:
            self._solver_params.SetDoubleParam(self._solver_params.PRESOLVE, presolve)

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
        self._solver.Add(constraint=expression.expr)
        return expression

    def set_objective(self, opt_type: OptimizationType, expression: Element) -> Element:
        if opt_type == OptimizationType.MINIMIZE:
            self._solver.Minimize(expr=expression.expr)
        elif opt_type == OptimizationType.MAXIMIZE:
            self._solver.Maximize(expr=expression.expr)
        else:
            raise ORToolsException('Invalid optimization type.')
        return expression

    def solve(self) -> None:
        self._status = self._solver.Solve(self._solver_params)

    def clear(self) -> None:
        self._solver.Clear()
