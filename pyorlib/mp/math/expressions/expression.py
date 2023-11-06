from typing import Any

from pyorlib.mp.math import Element


class Expression(Element):
    """
    Represents a mathematical expression used to encapsulate expressions in an optimization package.
    Provides methods for working with mathematical operations.
    """

    @property
    def expr(self) -> Any:
        return self.__expression

    def __init__(self, expression: Any):
        """
        Initialize an Expression instance.
        :param expression: The expression value to be encapsulated.
        :raises ValueError: If the expression is None.
        """

        if expression is None:
            raise ValueError("Expressions cannot be None")

        self.__expression: Any = expression
        """ The mathematical statement. """

    def _build_expression(self, expression: Any) -> Element:
        return Expression(expression=expression)

    def __str__(self) -> str:
        return str(self.expr)

    def __iadd__(self, other) -> Element:
        if isinstance(other, Element):
            self.__expression += other.expr
        else:
            self.__expression += other
        return self

    def __isub__(self, other) -> Element:
        if isinstance(other, Element):
            self.__expression -= other.expr
        else:
            self.__expression -= other
        return self

    def __imul__(self, other) -> Element:
        if isinstance(other, Element):
            self.__expression *= other.expr
        else:
            self.__expression *= other
        return self

    def __itruediv__(self, other) -> Element:
        if isinstance(other, Element):
            self.__expression /= other.expr
        else:
            self.__expression /= other
        return self

    def __ifloordiv__(self, other) -> Element:
        if isinstance(other, Element):
            self.__expression //= other.expr
        else:
            self.__expression //= other
        return self

    def __imod__(self, other) -> Element:
        if isinstance(other, Element):
            self.__expression %= other.expr
        else:
            self.__expression %= other
        return self

    def __ipow__(self, other) -> Element:
        if isinstance(other, Element):
            self.__expression **= other.expr
        else:
            self.__expression **= other
        return self
