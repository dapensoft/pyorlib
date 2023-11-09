from math import inf
from typing import Any

import gurobipy as gp

from pyorlib.mp.common.enums import ValueType
from pyorlib.mp.common.exceptions import GurobiException
from pyorlib.mp.common.validators import ValueTypeValidator
from pyorlib.mp.math.terms.variables.variable import Variable


class GurobiVariable(Variable):
    """
    Represents a Gurobi variable in an optimization model.

    The `GurobiVariable` class is a concrete implementation of the abstract `Variable` class.
    It represents a variable that is compatible with the Gurobi solver.
    """

    __slots__ = ["_gurobi_var"]

    @property
    def name(self) -> str:
        return self._gurobi_var.varName

    @property
    def lower_bound(self) -> float:
        lb = self._gurobi_var.getAttr('lb')
        return -inf if lb == gp.GRB.INFINITY else lb if lb != -0.0 else 0.0

    @property
    def upper_bound(self) -> float:
        ub = self._gurobi_var.getAttr('ub')
        return inf if ub == gp.GRB.INFINITY else ub if ub != -0.0 else 0.0

    @property
    def value(self) -> float:
        try:
            value: float = self._gurobi_var.getAttr('x')
            return value if value != -0.0 else 0.0
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
            lower_bound: float | None = None,
            upper_bound: float | None = None
    ):
        """
        Initializes a new `GurobiVariable` object with the specified attributes and creates a
        corresponding Gurobi variable.
        :param name: The name of the variable.
        :param solver: A reference to the Gurobi solver.
        :param value_type: An enumeration representing the type of the variable's value.
        :param lower_bound: The lower bound of the variable, or None. Default is 0.
        :param upper_bound: The upper bound of the variable, or None, to use the default. Default is infinity.
        """

        # Calls the super init method with the value type.
        super().__init__(value_type=value_type)

        if solver is None:
            raise GurobiException("The solver reference cannot be none.")
        if not name:
            raise GurobiException("Gurobi terms must have a name.")

        # Creates the Gurobi variable according to the value type
        gurobi_var: gp.Var

        if self.value_type == ValueType.BINARY:
            gurobi_var = solver.addVar(
                lb=0,
                ub=1,
                vtype=gp.GRB.BINARY,
                name=name,
                column=None,
                obj=0
            )
        elif self.value_type == ValueType.INTEGER:
            if lower_bound and not ValueTypeValidator.is_integer(lower_bound):
                raise GurobiException("Invalid lower bound value for a Gurobi integer variable.")
            if upper_bound and not ValueTypeValidator.is_integer(upper_bound):
                raise GurobiException("Invalid upper bound value for a Gurobi integer variable.")
            gurobi_var = solver.addVar(
                lb=lower_bound if lower_bound else 0,
                ub=upper_bound if upper_bound else gp.GRB.INFINITY,
                vtype=gp.GRB.INTEGER,
                name=name,
                column=None,
                obj=0
            )
        elif self.value_type == ValueType.CONTINUOUS:
            gurobi_var = solver.addVar(
                lb=lower_bound if lower_bound else 0,
                ub=upper_bound if upper_bound else gp.GRB.INFINITY,
                vtype=gp.GRB.CONTINUOUS,
                name=name,
                column=None,
                obj=0
            )
        else:
            raise GurobiException("Invalid term ValueType.")

        # Instance attributes
        self._gurobi_var: gp.Var = gurobi_var
        """ A gp.Var object representing the variable in the Gurobi solver. """

        if self._gurobi_var is None:
            raise GurobiException("Failed to create the gurobi variable.")

        # After creating the variable, we need to update the model in order
        # to gain access to the newly created variable. This is necessary
        # because Gurobi employs a lazy update approach.
        solver.update()

        # Apply validations.
        self.validate()
