from abc import ABC, abstractmethod
from typing import Any


class Element(ABC):
    """
    Base class representing a mathematical element.

    The `Element` class serves as the global interface for mathematical entities.
    Subclasses should inherit from this class and implement the required methods.

    **Note**: The supported mathematical operations on an `Element` instance depend on the
    specific entity being represented. These operations can include arithmetic operations,
    functions, and any other operations defined by the underlying mathematical element.
    """

    @property
    @abstractmethod
    def raw(self) -> Any:
        """
        Returns the raw representation of the mathematical element.

        The `raw` method, when implemented by subclasses, returns the mathematical element in its raw format.
        The raw format can take various forms, such as an expression used by solvers or engines, or a
        mathematical expression that represents the entity itself.
        :return: The raw representation of the mathematical element.
        """
        pass

    @abstractmethod
    def _build_expression(self, expression: Any) -> "Element":
        """
        Abstract method to build an Element object based on the given expression.

        This method is used to implement how an `Element` object is built based on the result of a Python magic
        method operation. It handles the construction of a new `Element` instance using the given expression,
        which represents the result of the operation. This method is used in the normal magic methods for
        mathematical operations, as well as the `right` methods and comparison methods. However, it
        excludes the in-place methods, as their behavior depends on whether they build another
        expression or modify the same expression.

        :param expression: The expression representing the result of the Python magic method operation.
        :return: A new `Element` instance representing the built expression.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the element.
        :return: A string representation of the element.
        """
        pass

    # Addition
    def __add__(self, other: Any) -> "Element":
        """
        Addition operation.
        :param other: The `number` or `Element` instance to be added.
        :return: A new `Element` instance representing the addition.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw + other.raw)
        else:
            return self._build_expression(expression=self.raw + other)

    def __radd__(self, other: Any) -> "Element":
        """
        Right addition operation.
        :param other: The `number` or `Element` instance to be added.
        :return: A new `Element` instance representing the addition.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=other.raw + self.raw)
        else:
            return self._build_expression(expression=other + self.raw)

    @abstractmethod
    def __iadd__(self, other: Any) -> "Element":
        """
        In-place addition operation.
        :param other: The `number` or `Element` instance to be added.
        :return: The updated Element instance after addition.
        """
        pass

    # Subtraction
    def __sub__(self, other: Any) -> "Element":
        """
        Subtraction operation.
        :param other: The `number` or `Element` instance to be subtracted.
        :return: A new `Element` instance representing the subtraction.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw - other.raw)
        else:
            return self._build_expression(expression=self.raw - other)

    def __rsub__(self, other: Any) -> "Element":
        """
        Right subtraction operation.
        :param other: The `number` or `Element` instance to be subtracted.
        :return: A new `Element` instance representing the subtraction.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=other.raw - self.raw)
        else:
            return self._build_expression(expression=other - self.raw)

    @abstractmethod
    def __isub__(self, other: Any) -> "Element":
        """
        In-place subtraction operation.
        :param other: The `number` or `Element` instance to be subtracted.
        :return: The new/updated `Element` instance after subtraction.
        """
        pass

    # Multiplication
    def __mul__(self, other: Any) -> "Element":
        """
        Multiplication operation.
        :param other: The `number` or `Element` instance to be multiplied.
        :return: A new `Element` instance representing the multiplication.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw * other.raw)
        else:
            return self._build_expression(expression=self.raw * other)

    def __rmul__(self, other: Any) -> "Element":
        """
        Right multiplication operation.
        :param other: The `number` or `Element` instance to be multiplied.
        :return: A new `Element` instance representing the multiplication.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=other.raw * self.raw)
        else:
            return self._build_expression(expression=other * self.raw)

    @abstractmethod
    def __imul__(self, other: Any) -> "Element":
        """
        In-place multiplication operation.
        :param other: The `number` or `Element` instance to be multiplied.
        :return: The new/updated `Element` instance after multiplication.
        """
        pass

    # Division
    def __truediv__(self, other: Any) -> "Element":
        """
        Division operation.
        :param other: The `number` or `Element` instance to be divided.
        :return: A new `Element` instance representing the division.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw / other.raw)
        else:
            return self._build_expression(expression=self.raw / other)

    def __rtruediv__(self, other: Any) -> "Element":
        """
        Right division operation.
        :param other: The `number` or `Element` instance to be divided.
        :return: A new `Element` instance representing the division.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=other.raw / self.raw)
        else:
            return self._build_expression(expression=other / self.raw)

    @abstractmethod
    def __itruediv__(self, other: Any) -> "Element":
        """
        In-place division operation.
        :param other: The `number` or `Element` instance to be divided.
        :return: The new/updated `Element` instance after division.
        """
        pass

    # Floor Division
    def __floordiv__(self, other: Any) -> "Element":
        """
        Floor division operation.
        :param other: The `number` or `Element` instance to be floor divided.
        :return: A new `Element` instance representing the floor division.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw // other.raw)
        else:
            return self._build_expression(expression=self.raw // other)

    def __rfloordiv__(self, other: Any) -> "Element":
        """
        Right floor division operation.
        :param other: The `number` or `Element` instance to be floor divided.
        :return: A new `Element` instance representing the floor division.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=other.raw // self.raw)
        else:
            return self._build_expression(expression=other // self.raw)

    @abstractmethod
    def __ifloordiv__(self, other: Any) -> "Element":
        """
        In-place floor division operation.
        :param other: The `number` or `Element` instance to be floor divided.
        :return: The new/updated `Element` instance after floor division.
        """
        pass

    # Modulo
    def __mod__(self, other: Any) -> "Element":
        """
        Modulo operation.
        :param other: The `number` or `Element` instance to be used for modulo.
        :return: A new `Element` instance representing the modulo operation.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw % other.raw)
        else:
            return self._build_expression(expression=self.raw % other)

    def __rmod__(self, other: Any) -> "Element":
        """
        Right modulo operation.
        :param other: The `number` or `Element` instance to be used for modulo.
        :return: A new `Element` instance representing the modulo operation.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=other.raw % self.raw)
        else:
            return self._build_expression(expression=other % self.raw)

    @abstractmethod
    def __imod__(self, other: Any) -> "Element":
        """
        In-place modulo operation.
        :param other: The `number` or `Element` instance to be used for modulo.
        :return: The new/updated `Element` instance after modulo operation.
        """
        pass

    # Exponentiation
    def __pow__(self, other: Any) -> "Element":
        """
        Exponentiation operation.
        :param other: The `number` or `Element` instance to be used as the exponent.
        :return: A new `Element` instance representing the exponentiation.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw**other.raw)
        else:
            return self._build_expression(expression=self.raw**other)

    def __rpow__(self, other: Any) -> "Element":
        """
        Right exponentiation operation.
        :param other: The `number` or `Element` instance to be used as the base.
        :return: A new `Element` instance representing the exponentiation.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=other.raw**self.raw)
        else:
            return self._build_expression(expression=other**self.raw)

    @abstractmethod
    def __ipow__(self, other: Any) -> "Element":
        """
        In-place exponentiation operation.
        :param other: The `number` or `Element` instance to be used as the exponent.
        :return: The new/updated `Element` instance after exponentiation.
        """
        pass

    # Unary Operators
    def __neg__(self) -> "Element":
        """
        Negation operation.
        :return: A new `Element` instance representing the negation.
        """
        return self._build_expression(expression=-self.raw)

    def __pos__(self) -> "Element":
        """
        Positive operation.
        :return: A new `Element` instance representing the positive value.
        """
        return self._build_expression(expression=+self.raw)

    def __abs__(self) -> "Element":
        """
        Absolute value operation.
        :return: A new `Element` instance representing the absolute value.
        """
        return self._build_expression(expression=abs(self.raw))

    # Comparison Methods
    def __eq__(self, other: Any) -> "Element":  # type: ignore[override]
        """
        Equal to comparison.
        :param other: The `number` or `Element` instance to be compared.
        :return: A new `Element` instance representing the comparison result.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw == other.raw)
        else:
            return self._build_expression(expression=self.raw == other)

    def __ne__(self, other: Any) -> "Element":  # type: ignore[override]
        """
        Not equal to comparison.
        :param other: The `number` or `Element` instance to be compared.
        :return: A new `Element` instance representing the comparison result.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw != other.raw)
        else:
            return self._build_expression(expression=self.raw != other)

    def __lt__(self, other: Any) -> "Element":
        """
        Less than comparison.
        :param other: The `number` or `Element` instance to be compared.
        :return: A new `Element` instance representing the comparison result.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw < other.raw)
        else:
            return self._build_expression(expression=self.raw < other)

    def __le__(self, other: Any) -> "Element":
        """
        Less than or equal to comparison.
        :param other: The `number` or `Element` instance to be compared.
        :return: A new `Element` instance representing the comparison result.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw <= other.raw)
        else:
            return self._build_expression(expression=self.raw <= other)

    def __gt__(self, other: Any) -> "Element":
        """
        Greater than comparison.
        :param other: The `number` or `Element` instance to be compared.
        :return: A new `Element` instance representing the comparison result.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw > other.raw)
        else:
            return self._build_expression(expression=self.raw > other)

    def __ge__(self, other: Any) -> "Element":
        """
        Greater than or equal to comparison.
        :param other: The `number` or `Element` instance to be compared.
        :return: A new `Element` instance representing the comparison result.
        """
        if isinstance(other, Element):
            return self._build_expression(expression=self.raw >= other.raw)
        else:
            return self._build_expression(expression=self.raw >= other)
