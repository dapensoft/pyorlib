from typing import Any

from ..element import Element


class Expression(Element):
    """
    Represents a mathematical expression used to encapsulate expressions in an optimization model.

    The `Expression` class is a subclass of the `Element` class and serves as a representation of a mathematical
    expression within an optimization model. It is specifically designed to encapsulate expressions and offers
    methods for performing various mathematical operations on those expressions.

    **Note**: The supported mathematical operations on an `Expression` instance depend on the operations supported
    in the encapsulated expression. These operations can include arithmetic operations, functions, and
    any other operations defined by the underlying mathematical expression.
    """

    @property
    def raw(self) -> Any:
        return self.__expression

    def __init__(self, expression: Any):
        """
        Initialize an Expression instance.
        :param expression: The expression value to be encapsulated.
        :raises ValueError: If the expression is None.
        """
        # Applies validations
        if expression is None:
            raise ValueError("Expression cannot be None")

        # Instance attributes
        self.__expression: Any = expression
        """ The mathematical expression. """

    def _build_expression(self, expression: Any) -> Element:
        return Expression(expression=expression)

    def __str__(self) -> str:
        return str(self.raw)

    def __iadd__(self, other: Any) -> Element:
        if isinstance(other, Element):
            self.__expression += other.raw
        else:
            self.__expression += other
        return self

    def __isub__(self, other: Any) -> Element:
        if isinstance(other, Element):
            self.__expression -= other.raw
        else:
            self.__expression -= other
        return self

    def __imul__(self, other: Any) -> Element:
        if isinstance(other, Element):
            self.__expression *= other.raw
        else:
            self.__expression *= other
        return self

    def __itruediv__(self, other: Any) -> Element:
        if isinstance(other, Element):
            self.__expression /= other.raw
        else:
            self.__expression /= other
        return self

    def __ifloordiv__(self, other: Any) -> Element:
        if isinstance(other, Element):
            self.__expression //= other.raw
        else:
            self.__expression //= other
        return self

    def __imod__(self, other: Any) -> Element:
        if isinstance(other, Element):
            self.__expression %= other.raw
        else:
            self.__expression %= other
        return self

    def __ipow__(self, other: Any) -> Element:
        if isinstance(other, Element):
            self.__expression **= other.raw
        else:
            self.__expression **= other
        return self
