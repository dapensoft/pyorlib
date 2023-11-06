from typing import List

import gurobipy as gp

from pyorlib.core.logger import StdOutLogger
from pyorlib.mp.common.enums import SolutionStatus, ValueType, OptimizationType
from pyorlib.mp.common.exceptions import GurobiException
from pyorlib.mp.engines.engine import Engine
from pyorlib.mp.math import Element
from pyorlib.mp.math.expressions import Expression
from pyorlib.mp.math.terms.variables import Variable
from pyorlib.mp.math.terms.variables.gurobi import GurobiVariable


class GurobiEngine(Engine):
    """
    This class provides a high-level interface for solving mathematical
    optimization problems using the Gurobi solver.
    """

    @property
    def name(self) -> str:
        return "Gurobi Engine"

    @property
    def constraints(self) -> List[Element]:
        return [Expression(expression=constraint) for constraint in self._solver.getConstrs()]

    @property
    def objective_value(self) -> float | None:
        if self.solution_status in [SolutionStatus.OPTIMAL, SolutionStatus.FEASIBLE]:
            return self._solver.getObjective().getValue()
        else:
            return None

    @property
    def objective_expr(self) -> Element | None:
        objective = self._solver.getObjective()
        return Expression(expression=objective) if objective is not None else None

    @property
    def solution_status(self) -> SolutionStatus:
        if self._solver.status == gp.GRB.LOADED:
            return SolutionStatus.NOT_SOLVED
        elif self._solver.status == gp.GRB.OPTIMAL:
            return SolutionStatus.OPTIMAL
        elif self._solver.status == gp.GRB.SUBOPTIMAL:
            return SolutionStatus.FEASIBLE
        elif self._solver.status == gp.GRB.INFEASIBLE:
            return SolutionStatus.INFEASIBLE
        elif self._solver.status in [gp.GRB.TIME_LIMIT, gp.GRB.NODE_LIMIT, gp.GRB.ITERATION_LIMIT,
                                     gp.GRB.SOLUTION_LIMIT, gp.GRB.INTERRUPTED, gp.GRB.UNBOUNDED]:
            return SolutionStatus.ERROR
        else:
            StdOutLogger.error(action="Solution status: ", msg=f"{self._solver.status}")
            raise GurobiException('Invalid solution status.')

    def __init__(
            self,
            time_limit: float | None = None,
            mip_gap: float | None = None,
            output_flag: bool | None = None,
            num_threads: int | None = None,
            presolve: int | None = None,
    ):
        """
        Initializes a new instance of the GurobiSolver class.
        :param time_limit: Maximum time limit for the solver to find an optimal solution (in seconds). Default is None (use solver default).
        :param mip_gap: Relative MIP optimality gap. Default is None (use solver default).
        :param output_flag: Enables or disables solver output. Default is None (use solver default).
        :param num_threads: Number of parallel threads to use. Default is None (use solver default).
        :param presolve: Controls the presolve level. A value of -1 corresponds to an automatic setting. Other options are off (0), conservative (1), or aggressive (2). Default is None (use solver default).
        """

        # Instance attributes
        self._solver: gp.Model = gp.Model()
        """ A reference to the Gurobi solver. """

        if self._solver is None:
            GurobiException("Failed to create the gurobi solver.")

        self._solver.setParam('OutputFlag', 0)

        # Set solver configuration
        if time_limit is not None:
            self._solver.setParam('TimeLimit', time_limit)
        if mip_gap is not None:
            self._solver.setParam('MIPGap', mip_gap)
        if output_flag is not None:
            self._solver.setParam('OutputFlag', output_flag)
        if num_threads is not None:
            self._solver.setParam('Threads', num_threads)
        if presolve is not None:
            self._solver.setParam('Presolve', presolve)

    def add_variable(
            self,
            name: str,
            value_type: ValueType,
            lower_bound: float | None = None,
            upper_bound: float | None = None
    ) -> Variable:
        return GurobiVariable(
            name=name,
            solver=self._solver,
            value_type=value_type,
            lower_bound=lower_bound,
            upper_bound=upper_bound
        )

    def add_constraint(self, expression: Element) -> Element:
        self._solver.addConstr(expression.expr, name="")
        self._solver.update()
        return expression

    def set_objective(self, opt_type: OptimizationType, expression: Element) -> Element:
        if opt_type == OptimizationType.MINIMIZE:
            self._solver.setObjective(expression.expr, gp.GRB.MINIMIZE)
        elif opt_type == OptimizationType.MAXIMIZE:
            self._solver.setObjective(expression.expr, gp.GRB.MAXIMIZE)
        else:
            raise GurobiException("Invalid optimization type.")
        self._solver.update()
        return expression

    def solve(self) -> None:
        self._solver.optimize()

    def clear(self) -> None:
        self._solver.dispose()
