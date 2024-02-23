from math import inf
from typing import List, Any

from ..engine import Engine
from ...algebra import Element
from ...algebra.expressions import Expression
from ...algebra.terms.variables import Variable
from ...core.loggers import StdOutLogger
from ...enums import SolutionStatus, ValueType, OptimizationType
from ...exceptions import GurobiException

try:  # pragma: no cover
    import gurobipy as gp
except ImportError:  # pragma: no cover
    raise GurobiException(
        "Optional dependency 'Gurobi' not found.\nPlease install it using 'pip install pyorlib[gurobi]'."
    )


class GurobiEngine(Engine):
    """
    Concrete engine implementation using Gurobi solver.

    This class provides an interface for formulating and solving linear,
    integer, and nonlinear optimization models using the Gurobi optimizer.
    """

    class _Variable(Variable):
        """
        Represents a Gurobi variable in an optimization model.

        The `GurobiVariable` class is a concrete implementation of the abstract `Variable` class.
        It represents a variable that is compatible with the Gurobi solver.
        """

        __slots__ = ["_gurobi_var"]

        @property
        def name(self) -> str:
            return str(self._gurobi_var.VarName)

        @property
        def lower_bound(self) -> float:
            lb = self._gurobi_var.getAttr("lb")
            return -inf if lb == gp.GRB.INFINITY else float(lb) if lb != -0.0 else 0.0

        @property
        def upper_bound(self) -> float:
            ub = self._gurobi_var.getAttr("ub")
            return inf if ub == gp.GRB.INFINITY else float(ub) if ub != -0.0 else 0.0

        @property
        def value(self) -> float:
            try:
                value = self._gurobi_var.getAttr("x")
                return float(value) if value != -0.0 else 0.0  # pragma: no cover
            except AttributeError:
                return -0.0

        @property
        def raw(self) -> Any:
            return self._gurobi_var

        def __init__(
            self,
            name: str,
            solver: gp.Model,
            value_type: ValueType,
            lower_bound: float = 0,
            upper_bound: float = inf,
        ):
            """
            Initializes a new `GurobiVariable` object with the specified attributes and creates a
            corresponding Gurobi variable.
            :param name: The name of the variable.
            :param solver: A reference to the Gurobi solver.
            :param value_type: An enumeration representing the type of the variable's value.
            :param lower_bound: The lower bound of the variable. Default is 0.
            :param upper_bound: The upper bound of the variable. Default is infinity.
            """
            # Calls the super init method and its validations
            super().__init__(name=name, value_type=value_type, lower_bound=lower_bound, upper_bound=upper_bound)

            # Applies new validations
            if solver is None:
                raise GurobiException("The 'solver' argument cannot be None.")

            # Creates the Gurobi variable according to the value type
            gurobi_var: gp.Var | None

            if self.value_type == ValueType.BINARY:
                gurobi_var = solver.addVar(lb=0, ub=1, vtype=gp.GRB.BINARY, name=name, column=None, obj=0)
            elif self.value_type == ValueType.INTEGER:
                gurobi_var = solver.addVar(
                    lb=lower_bound,
                    ub=upper_bound,
                    vtype=gp.GRB.INTEGER,
                    name=name,
                    column=None,
                    obj=0,
                )
            elif self.value_type == ValueType.CONTINUOUS:
                gurobi_var = solver.addVar(
                    lb=lower_bound,
                    ub=upper_bound,
                    vtype=gp.GRB.CONTINUOUS,
                    name=name,
                    column=None,
                    obj=0,
                )
            else:
                raise GurobiException("Unknown ValueType.")

            # Applies new validations
            if gurobi_var is None:
                raise GurobiException("Failed to create the Gurobi variable.")

            # Instance attributes
            self._gurobi_var: gp.Var = gurobi_var
            """ A gp.Var object representing the variable in the Gurobi solver. """

            # After creating the variable, we need to update the model in order
            # to gain access to the newly created variable. This is necessary
            # because Gurobi employs a lazy update approach.
            solver.update()

    @property
    def name(self) -> str:  # pragma: no cover
        return "Gurobi Engine"

    @property
    def constraints(self) -> List[Element]:
        return [Expression(expression=constraint) for constraint in self._solver.getConstrs()]

    @property
    def objective_value(self) -> float | None:
        if self.solution_status in [SolutionStatus.OPTIMAL, SolutionStatus.FEASIBLE]:
            return float(self._solver.getObjective().getValue())
        return None

    @property
    def objective_expr(self) -> Element | None:
        objective = self._solver.getObjective()
        return Expression(expression=objective) if objective is not None else None

    @property
    def solution_status(self) -> SolutionStatus:  # pragma: no cover
        if self._solver.status == gp.GRB.LOADED:
            return SolutionStatus.NOT_SOLVED
        elif self._solver.status == gp.GRB.OPTIMAL:
            return SolutionStatus.OPTIMAL
        elif self._solver.status == gp.GRB.SUBOPTIMAL:
            return SolutionStatus.FEASIBLE
        elif self._solver.status == gp.GRB.INFEASIBLE:
            return SolutionStatus.INFEASIBLE
        elif self._solver.status in [
            gp.GRB.TIME_LIMIT,
            gp.GRB.NODE_LIMIT,
            gp.GRB.ITERATION_LIMIT,
            gp.GRB.SOLUTION_LIMIT,
            gp.GRB.INTERRUPTED,
            gp.GRB.UNBOUNDED,
        ]:
            return SolutionStatus.ERROR
        else:
            StdOutLogger.error(action="Solution status: ", msg=f"{self._solver.status}")
            raise GurobiException("Unhandled Gurobi status code.")

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

        if self._solver is None or not isinstance(self._solver, gp.Model):
            raise GurobiException("The Gurobi solver must be an instance of gp.Model")

        self._solver.setParam("OutputFlag", 0)

    def add_variable(
        self,
        name: str,
        value_type: ValueType,
        lower_bound: float = 0,
        upper_bound: float = inf,
    ) -> Variable:
        return GurobiEngine._Variable(
            name=name, solver=self._solver, value_type=value_type, lower_bound=lower_bound, upper_bound=upper_bound
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
