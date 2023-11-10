from typing import List

import gurobipy as gp

from src.pyorlib.core.loggers import StdOutLogger
from src.pyorlib.mp.algebra import Element
from src.pyorlib.mp.algebra.expressions import Expression
from src.pyorlib.mp.algebra.terms.variables import Variable
from src.pyorlib.mp.algebra.terms.variables.gurobi import GurobiVariable
from src.pyorlib.mp.engines.engine import Engine
from src.pyorlib.mp.enums import SolutionStatus, ValueType, OptimizationType
from src.pyorlib.mp.exceptions import GurobiException


class GurobiEngine(Engine):
    """
    Concrete engine implementation using Gurobi solver.

    This class provides an interface for formulating and solving linear,
    integer, and nonlinear optimization models using the Gurobi optimizer.
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
            raise GurobiException('Unhandled Gurobi status code.')

    def __init__(self, solver: gp.Model | None = None):
        """
        Initializes a new GurobiEngine instance.

        The solver parameter allows customizing the underlying Gurobi solver.
        :param solver: A Gurobi solver object. If None, a new solver
            will be instantiated using the Gurobipy default settings.
            Allows customizing the solver configuration and behavior.
        """

        # Instance attributes
        self._solver: gp.Model = solver if solver else gp.Model()
        """ A reference to the Gurobi solver. """

        if self._solver is None:
            raise GurobiException("The Gurobi solver cannot be None.")

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
        self._solver.addConstr(expression.raw, name="")
        self._solver.update()
        return expression

    def set_objective(self, opt_type: OptimizationType, expression: Element) -> Element:
        if opt_type == OptimizationType.MINIMIZE:
            self._solver.setObjective(expression.raw, gp.GRB.MINIMIZE)
        elif opt_type == OptimizationType.MAXIMIZE:
            self._solver.setObjective(expression.raw, gp.GRB.MAXIMIZE)
        else:
            raise GurobiException("Optimization type not supported.")
        self._solver.update()
        return expression

    def solve(self) -> None:
        self._solver.optimize()

    def clear(self) -> None:
        self._solver.dispose()
