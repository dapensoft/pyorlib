from typing import List

import gurobipy as gp

from pyorlib.core.loggers import StdOutLogger
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
            solver: gp.Model | None = None,
    ):
        """
        Initializes a new instance of the GurobiSolver class.
        :param solver: Specifies a Gurobi solver to be used by the engine. Default is None (instantiates a default solver).
        """

        # Instance attributes
        self._solver: gp.Model = solver if solver else gp.Model()
        """ A reference to the Gurobi solver. """

        if self._solver is None:
            GurobiException("Failed to create the gurobi solver.")

        self._solver.setParam('OutputFlag', 0)

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
