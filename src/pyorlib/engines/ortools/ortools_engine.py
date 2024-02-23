from math import inf
from typing import List, Any, Callable

from ..engine import Engine
from ...algebra import Element
from ...algebra.expressions import Expression
from ...algebra.terms.variables import Variable
from ...core.loggers import StdOutLogger
from ...enums import SolutionStatus, ValueType, OptimizationType
from ...exceptions import ORToolsException

try:  # pragma: no cover
    from ortools.linear_solver.pywraplp import Solver, MPSolverParameters, Variable as ORToolsVar
except ImportError:  # pragma: no cover
    raise ORToolsException(
        "Optional dependency 'OR-Tools' not found.\nPlease install it using 'pip install pyorlib[ortools]'."
    )


class ORToolsEngine(Engine):
    """
    Concrete engine implementation using Google's OR-Tools linear programming solver.

    This class provides an interface for formulating and solving linear and
    integer programming models using the OR-Tools solver.
    """

    class _Variable(Variable):
        """
        Represents a OR-Tools variable in an optimization model.

        The `ORToolsVariable` class is a concrete implementation of the abstract `Variable` class.
        It represents a variable that is compatible with the OR-Tools solver.
        """

        __slots__ = ["_ortools_var", "_solution_status"]

        @property
        def name(self) -> str:
            return str(self._ortools_var.name())

        @property
        def lower_bound(self) -> float:
            return float(self._ortools_var.lb())

        @property
        def upper_bound(self) -> float:
            return float(self._ortools_var.ub())

        @property
        def value(self) -> float:
            if self._solution_status() in [SolutionStatus.OPTIMAL, SolutionStatus.FEASIBLE]:
                return float(round(self._ortools_var.solution_value(), 6))
            else:
                return -0.0

        @property
        def raw(self) -> Any:
            return self._ortools_var

        def __init__(
            self,
            name: str,
            solver: Solver,
            value_type: ValueType,
            solution_status: Callable[[], SolutionStatus],
            lower_bound: float = 0,
            upper_bound: float = inf,
        ):
            """
            Initializes a new `ORToolsVariable` object with the specified attributes and creates a
            corresponding OR-Tools variable.
            :param name: The name of the variable.
            :param solver: A reference to the OR-Tools solver.
            :param value_type: An enumeration representing the type of the variable's value.
            :param solution_status: A callable function that returns the current solution status.
            :param lower_bound: The lower bound of the variable. Default is 0.
            :param upper_bound: The upper bound of the variable. Default is infinity.
            """
            # Calls the super init method and its validations
            super().__init__(name=name, value_type=value_type, lower_bound=lower_bound, upper_bound=upper_bound)

            # Applies new validations
            if solver is None:
                raise ORToolsException("The 'solver' argument cannot be None.")

            # Creates the OR-Tools variable according to the value type
            ortools_var: ORToolsVar | None

            if self.value_type == ValueType.BINARY:
                ortools_var = solver.BoolVar(name=name)
            elif self.value_type == ValueType.INTEGER:
                ortools_var = solver.IntVar(name=name, lb=lower_bound, ub=upper_bound)
            elif self.value_type == ValueType.CONTINUOUS:
                ortools_var = solver.NumVar(name=name, lb=lower_bound, ub=upper_bound)
            else:
                raise ORToolsException("Unknown ValueType.")

            # Applies new validations
            if solution_status is None:
                raise ORToolsException("The 'solution_status' argument cannot be None.")

            if ortools_var is None:
                raise ORToolsException("Failed to create the OR-Tools variable.")

            # Instance attributes
            self._solution_status: Callable[[], SolutionStatus] = solution_status
            """ A callable to check the current status of the solution. """

            self._ortools_var: ORToolsVar = ortools_var
            """ A pywraplp.Variable object representing the variable in the OR-Tools solver. """

    @property
    def name(self) -> str:  # pragma: no cover
        return "OR-Tools Engine"

    @property
    def constraints(self) -> List[Element]:
        return [Expression(expression=constraint) for constraint in self._solver.constraints()]

    @property
    def objective_value(self) -> float | None:
        if self.solution_status in [SolutionStatus.OPTIMAL, SolutionStatus.FEASIBLE]:
            return float(self._solver.Objective().Value())
        return None

    @property
    def objective_expr(self) -> Element | None:
        objective = self._solver.Objective()
        return Expression(expression=objective) if objective is not None else None

    @property
    def solution_status(self) -> SolutionStatus:  # pragma: no cover
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
            raise ORToolsException("Unhandled OR-Tools status code.")

    def __init__(self, solver: Solver | None = None, solver_params: MPSolverParameters | None = None):
        """
        Initializes a new instance of the ORToolsEngine class.

        The solver and solver_params parameters enable customizing the
        underlying OR-Tools solver and its configuration.
        :param solver: An OR-Tools Solver object. If None, a new OR-Tools Solver
            will be instantiated using SCIP as its backend solver.
            Allows customizing the solver type (e.g. GLOP, SCIP).
        :param solver_params: OR-Tools solver parameters object. If None,
            default parameters will be used. Allows customizing the
            solver configuration.
        """

        # Instance attributes
        self._solver: Solver = solver if solver else Solver.CreateSolver(solver_id="SCIP")
        """ A reference to the OR-Tools solver. """

        # Set or tools configuration
        self._solver_params: MPSolverParameters = solver_params if solver_params else MPSolverParameters()

        self._status: int = 6
        """ Represents the state of the solution. """

        if self._solver is None or not isinstance(self._solver, Solver):
            raise ORToolsException("The OR-Tools solver cannot be None.")

        if self._solver_params is None:  # pragma: no cover
            raise ORToolsException("The OR-Tools params cannot be None.")

    def add_variable(
        self,
        name: str,
        value_type: ValueType,
        lower_bound: float = 0,
        upper_bound: float = inf,
    ) -> Variable:
        return ORToolsEngine._Variable(
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
            raise ORToolsException("Optimization type not supported.")
        return expression

    def solve(self) -> None:
        self._status = self._solver.Solve(self._solver_params)
