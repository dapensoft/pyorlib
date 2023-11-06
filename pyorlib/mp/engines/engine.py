from abc import ABC, abstractmethod
from typing import List

from pyorlib.mp.common.enums import SolutionStatus, ValueType, OptimizationType
from pyorlib.mp.math import Element
from pyorlib.mp.math.terms.variables import Variable


class Engine(ABC):
    """
    The Engine class is an abstract class representing an optimization engine
    for mathematical models.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Returns the name of the solver that is currently being used to solve an optimization problem.
        :return: A string with name of the solver.
        """
        pass

    @property
    @abstractmethod
    def constraints(self) -> List[Element]:
        """
        Returns a list of all constraints in the optimization model.
        :return: A list of constraints in the optimization model.
        """
        pass

    @property
    @abstractmethod
    def objective_value(self) -> float | None:
        """
        Returns the value of the objective function for the current solution, if available.
        :return: The value of the objective function, or None if not available.
        """
        pass

    @property
    @abstractmethod
    def objective_expr(self) -> Element | None:
        """
        Returns the expression of the objective function, if available.
        :return: The objective function, or None if not available.
        """
        pass

    @property
    @abstractmethod
    def solution_status(self) -> SolutionStatus:
        """
        Returns an enumeration that represents the state of the solution.
        :return: A SolutionStatus enumeration.
        """
        pass

    @abstractmethod
    def add_variable(
            self,
            name: str,
            value_type: ValueType,
            lower_bound: float | None = None,
            upper_bound: float | None = None
    ) -> Variable:
        """
        Adds a variable to the optimization problem with the specified value type and bounds.
        :param name: The name of the variable.
        :param value_type: The value type of the variable.
        :param lower_bound: The lower bound of the variable value. The default is 0.
        :param upper_bound: The upper bound of the variable value. The default is infinity.
        :return: Returns a BaseTerm Variable.
        """
        pass

    @abstractmethod
    def add_constraint(self, expression: Element) -> Element:
        """
        Adds a constraint to the optimization problem.
        :param expression: The constraint expression.
        :return: An object representing the constraint.
        """
        pass

    @abstractmethod
    def set_objective(self, opt_type: OptimizationType, expression: Element) -> Element:
        """
        Sets the objective function for the optimization problem.
        :param opt_type: The type of optimization to be performed.
        :param expression: The expression of the objective function.
        :return: The objective function.
        """
        pass

    @abstractmethod
    def solve(self) -> None:
        """
        Solves the optimization problem using the specified solver.
        :return: None
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """
        Clears the optimization problem by removing all variables,
        constraints, and objective function.
        :return: None
        """
        pass
