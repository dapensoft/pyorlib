from math import inf
from typing import List, Any

from ..engine import Engine
from ...algebra import Element
from ...algebra.expressions import Expression
from ...algebra.terms.variables import Variable
from ...core.loggers import StdOutLogger
from ...enums import SolutionStatus, ValueType, OptimizationType
from ...exceptions import CplexException

try:  # pragma: no cover
    import docplex.mp.model as cpx
    from docplex.mp.dvar import Var
    from docplex.mp.utils import DOcplexException
except ImportError:  # pragma: no cover
    raise CplexException(
        "Optional dependency 'CPLEX' not found.\nPlease install it using 'pip install pyorlib[cplex]'."
    )


class CplexEngine(Engine):
    """
    Concrete engine implementation using IBM CPLEX optimizer.

    This class provides an interface for formulating and solving linear,
    integer, and nonlinear optimization models using the CPLEX solver.
    """

    class _Variable(Variable):
        """
        Represents a CPLEX variable in an optimization model.

        The `CplexVariable` class is a concrete implementation of the abstract `Variable` class.
        It represents a variable that is compatible with the CPLEX solver.
        """

        # Strict class attributes.
        __slots__ = ["_cplex_var"]

        @property
        def name(self) -> str:
            return str(self._cplex_var.name)

        @property
        def lower_bound(self) -> float:
            lb = self._cplex_var.lb
            return -inf if lb <= -1e20 else float(lb)

        @property
        def upper_bound(self) -> float:
            ub = self._cplex_var.ub
            return inf if ub >= 1e20 else float(ub)

        @property
        def value(self) -> float:
            try:
                return float(self._cplex_var.solution_value)
            except DOcplexException:
                return -0.0

        @property
        def raw(self) -> Any:
            return self._cplex_var

        def __init__(
            self,
            name: str,
            solver: cpx.Model,
            value_type: ValueType,
            lower_bound: float = 0,
            upper_bound: float = inf,
        ):
            """
            Initializes a new `CplexVariable` object with the specified attributes and creates a corresponding CPLEX
            variable in the specified CPLEX solver.
            :param name: The name of the variable.
            :param solver: A reference to the CPLEX solver.
            :param value_type: An enumeration representing the type of the variable's value.
            :param lower_bound: The lower bound of the variable. Default is 0.
            :param upper_bound: The upper bound of the variable. Default is infinity.
            """
            # Calls the super init method and its validations
            super().__init__(name=name, value_type=value_type, lower_bound=lower_bound, upper_bound=upper_bound)

            # Applies new validations
            if solver is None:
                raise CplexException("The 'solver' argument cannot be None.")

            # Creates the CPLEX variable according to the value type
            cplex_var: Var | None

            if self.value_type == ValueType.BINARY:
                cplex_var = solver.binary_var(name=name)
            elif self.value_type == ValueType.INTEGER:
                cplex_var = solver.integer_var(name=name, lb=lower_bound, ub=upper_bound)
            elif self.value_type == ValueType.CONTINUOUS:
                cplex_var = solver.continuous_var(name=name, lb=lower_bound, ub=upper_bound)
            else:
                raise CplexException("Unknown ValueType.")

            # Applies new validations
            if cplex_var is None:
                raise CplexException("Failed to create the CPLEX variable.")

            # Instance attributes
            self._cplex_var: Var = cplex_var
            """ A Cplex.Var object representing the variable in the CPLEX solver. """

    @property
    def name(self) -> str:  # pragma: no cover
        return "CPLEX Engine"

    @property
    def constraints(self) -> List[Element]:
        return [Expression(expression=constraint) for constraint in self._solver.iter_constraints()]

    @property
    def objective_value(self) -> float | None:
        if self.solution_status in [SolutionStatus.OPTIMAL, SolutionStatus.FEASIBLE]:
            return float(self._solver.objective_value)
        return None

    @property
    def objective_expr(self) -> Element | None:
        objective = self._solver.get_objective_expr()
        return Expression(expression=objective) if objective is not None else None

    @property
    def solution_status(self) -> SolutionStatus:  # pragma: no cover
        if self._solver.solve_details is None:
            return SolutionStatus.NOT_SOLVED

        # Status Codes
        optimal_codes = [1, 5, 15, 17, 19, 20, 101, 102, 115, 121, 123, 125, 129, 130, 301]
        feasible_codes = [14, 16, 18, 23, 30, 120, 124, 127]
        infeasible_codes = [3, 103]

        if self._solver.solve_details.status_code in optimal_codes:
            return SolutionStatus.OPTIMAL
        elif self._solver.solve_details.status_code in feasible_codes:
            return SolutionStatus.FEASIBLE
        elif self._solver.solve_details.status_code in infeasible_codes:
            return SolutionStatus.INFEASIBLE
        else:
            StdOutLogger.error(action="Error code: ", msg=f"{self._solver.solve_details.status_code}")
            return SolutionStatus.ERROR

    def __init__(self, solver: cpx.Model | None = None):
        """
        Initialize a CPLEX engine instance.
        :param solver: A CPLEX solver object. If None, a new solver will be
            instantiated using CPLEX's default settings. Allows custom
            configuration of the solver before passing to the engine.
        """

        # Instance attributes
        self._solver: cpx.Model = solver if solver else cpx.Model(log_output=False)
        """ A reference to the CPLEX solver. """

        if self._solver is None or not isinstance(self._solver, cpx.Model):
            raise CplexException("The CPLEX solver must be an instance of cpx.Model")

    def add_variable(
        self,
        name: str,
        value_type: ValueType,
        lower_bound: float = 0,
        upper_bound: float = inf,
    ) -> Variable:
        return CplexEngine._Variable(
            name=name,
            solver=self._solver,
            value_type=value_type,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
        )

    def add_constraint(self, expression: Element) -> Element:
        self._solver.add_constraint(ct=expression.raw)
        return expression

    def set_objective(self, opt_type: OptimizationType, expression: Element) -> Element:
        if opt_type == OptimizationType.MINIMIZE:
            self._solver.minimize(expr=expression.raw)
        elif opt_type == OptimizationType.MAXIMIZE:
            self._solver.maximize(expr=expression.raw)
        else:
            raise CplexException("Optimization type not supported.")
        return expression

    def solve(self) -> None:
        self._solver.solve()
