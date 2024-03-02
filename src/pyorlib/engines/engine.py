from abc import ABC, abstractmethod
from math import inf
from typing import List

from ..algebra import Element
from ..algebra.terms.variables import Variable
from ..enums import SolutionStatus, ValueType, OptimizationType


class Engine(ABC):
    """
    Abstract base class for optimization engines.

    The `Engine` class is a base class that provides a common interface for interacting with different solvers. It
    serves as a foundation for representing and utilizing various solver implementations, such as Gurobi, CPLEX,
    and others.

    By inheriting from this base class, specific engine classes can be developed to implement solver-specific
    functionality while adhering to the common interface defined by the `Engine` class.

    This decoupling from the specific solvers allows for greater flexibility and interchangeability of solver
    implementations within an optimization model. It promotes code reuse and simplifies the process of integrating
    different solvers into an application.

    The `Engine` class defines a set of abstract methods that must be implemented by concrete engine classes. These
    methods include solving the optimization model, adding variables and constraints, setting the objective function,
    and configuring solver-specific parameters.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the name of the concrete solver.
        :return: The name of the concrete solver implementation.
        """
        pass

    @property
    @abstractmethod
    def constraints(self) -> List[Element]:
        """
        Get the list of constraints in the model.
        :return: The list of constraint objects.
        """
        pass

    @property
    @abstractmethod
    def objective_value(self) -> float | None:
        """
        Get the objective value for the current solution.
        :return: The objective value, or None if no solution exists.
        """
        pass

    @property
    @abstractmethod
    def objective_expr(self) -> Element | None:
        """
        Get the objective expression object.
        :return: The objective expression, or None if not set.
        """
        pass

    @property
    @abstractmethod
    def solution_status(self) -> SolutionStatus:
        """
        Get the solution status.
        :return: The status of the current solution.
        """
        pass

    @abstractmethod
    def add_variable(
        self,
        name: str,
        value_type: ValueType,
        lower_bound: float = 0,
        upper_bound: float = inf,
    ) -> Variable:
        """
        Add a new variable to the engine.
        :param name: The name of the variable.
        :param value_type: The value type of the variable.
        :param lower_bound: The lower bound of the variable. Default is 0.
        :param upper_bound: The upper bound of the variable. Default is infinity.
        :return: The created variable object.
        """
        pass

    @abstractmethod
    def add_constraint(self, expression: Element) -> Element:
        """
        Add a new constraint expression to the engine.
        :param expression: The constraint expression.
        :return: The created constraint object.
        """
        pass

    @abstractmethod
    def set_objective(self, opt_type: OptimizationType, expression: Element) -> Element:
        """
        Defines the objective function.
        :param opt_type: The type of optimization to be performed.
        :param expression: The objective expression.
        :return: The objective function.
        """
        pass

    @abstractmethod
    def solve(self) -> None:
        """
        Solve the optimization model.
        :return: None
        """
        pass
