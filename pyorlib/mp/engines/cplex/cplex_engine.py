from typing import List

import docplex.mp.model as cpx

from pyorlib.core.logger import StdOutLogger
from pyorlib.mp.common.enums import SolutionStatus, ValueType, OptimizationType
from pyorlib.mp.common.exceptions import CplexException
from pyorlib.mp.engines.engine import Engine
from pyorlib.mp.math import Element
from pyorlib.mp.math.expressions import Expression
from pyorlib.mp.math.terms.variables import Variable
from pyorlib.mp.math.terms.variables.cplex import CplexVariable


class CplexEngine(Engine):
    """
    This class provides a high-level interface for solving mathematical
    optimization problems using the Cplex solver.
    """

    @property
    def name(self) -> str:
        return "Cplex Solver"

    @property
    def constraints(self) -> List[Element]:
        return [Expression(expression=constraint) for constraint in self._solver.iter_constraints()]

    @property
    def objective_value(self) -> float | None:
        if self.solution_status in [SolutionStatus.OPTIMAL, SolutionStatus.FEASIBLE]:
            return self._solver.objective_value
        return None

    @property
    def objective_expr(self) -> Element | None:
        objective = self._solver.get_objective_expr()
        return Expression(expression=objective) if objective is not None else None

    @property
    def solution_status(self) -> SolutionStatus:
        if self._solver.solve_details is None:
            return SolutionStatus.NOT_SOLVED

        if self._solver.solve_details.status_code in [1, 5, 15, 17, 19, 20, 101, 102, 115, 121, 123, 125, 129, 130,
                                                      301]:
            return SolutionStatus.OPTIMAL
        elif self._solver.solve_details.status_code in [14, 16, 18, 23, 30, 120, 124, 127]:
            return SolutionStatus.FEASIBLE
        elif self._solver.solve_details.status_code in [3, 103]:
            return SolutionStatus.INFEASIBLE
        elif self._solver.solve_details.status_code in [10, 11, 12, 13, 21, 22, 25, 32, 33, 34, 35, 36, 37, 38, 39, 113,
                                                        114, 126, 133, 2, 118, 133, 304]:
            return SolutionStatus.ERROR
        else:
            StdOutLogger.error(action="Solution status: ", msg=f"{self._solver.solve_details.status_code}")
            raise CplexException('Invalid cplex status code.')

    def __init__(
            self,
            time_limit: float | None = None,
            mip_gap: float | None = None,
            logging: bool | None = None,
            num_threads: int | None = None,
            presolve: bool | None = None,
    ):
        """
        Initializes a new instance of the CplexSolver class.
        :param time_limit: Maximum time limit for the solver to find an optimal solution (in seconds). Default is None (use solver default).
        :param mip_gap: Relative MIP optimality gap. Default is None (use solver default).
        :param logging: Enables or disables solver output. Default is None (use solver default).
        :param num_threads: Number of parallel threads to use. Default is None (use solver default).
        :param presolve: Controls the presolve of the model to produce more compact formulations and to achieve more domain reduction. Default is None (use solver default).
        """

        # Instance attributes
        self._solver: cpx.Model = cpx.Model(log_output=logging)
        """ A reference to the CPLEX solver. """

        if self._solver is None:
            CplexException("Failed to create the cplex solver.")

        # Set solver configuration
        if time_limit is not None:
            self._solver.set_time_limit(time_limit)
        if mip_gap is not None:
            self._solver.parameters.mip.tolerances.mipgap = mip_gap
        if num_threads is not None:
            self._solver.parameters.threads = num_threads
        if presolve is not None:
            self._solver.parameters.preprocessing.presolve = presolve

    def add_variable(
            self,
            name: str,
            value_type: ValueType,
            lower_bound: float | None = None,
            upper_bound: float | None = None
    ) -> Variable:
        return CplexVariable(
            name=name,
            solver=self._solver,
            value_type=value_type,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )

    def add_constraint(self, expression: Element) -> Element:
        self._solver.add_constraint(ct=expression.expr)
        return expression

    def set_objective(self, opt_type: OptimizationType, expression: Element) -> Element:
        if opt_type == OptimizationType.MINIMIZE:
            self._solver.minimize(expr=expression.expr)
        elif opt_type == OptimizationType.MAXIMIZE:
            self._solver.maximize(expr=expression.expr)
        else:
            raise CplexException("Invalid optimization type.")
        return expression

    def solve(self) -> None:
        self._solver.solve()

    def clear(self) -> None:
        self._solver.clear()
