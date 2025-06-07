from math import isclose

from pytest import raises

from pyorlib.algebra import Element, Expression


class TestExpression:

    def test_inheritance(self):
        assert issubclass(Expression, Element)

    def test_creation_with_empty_expression(self):
        with raises(Exception):
            Expression(expression=None)

    def test_expression_property(self):
        expr1: Expression = Expression(expression=7)

        assert isinstance(expr1, Element)
        assert expr1.raw == 7
        assert str(expr1) == str(expr1.raw)

    def test_iadd_operation(self):
        # Test creation
        expr1: Expression = Expression(expression=3)
        expr2: Expression = Expression(expression=9)

        # Test __iadd__ method
        expr1 += expr1
        expr2 += 3

        assert isinstance(expr1, Expression)
        assert isinstance(expr2, Expression)
        assert expr1.raw == 6
        assert expr2.raw == 12

    def test_isub_operation(self):
        # Test creation
        expr1: Expression = Expression(expression=2)
        expr2: Expression = Expression(expression=-11)

        # Test __isub__ method
        expr1 -= expr1
        expr2 -= 5

        assert isinstance(expr1, Expression)
        assert isinstance(expr2, Expression)
        assert expr1.raw == 0
        assert expr2.raw == -16

    def test_imul_operation(self):
        # Test creation
        expr1: Expression = Expression(expression=-4)
        expr2: Expression = Expression(expression=-3)

        # Test __imul__ method
        expr1 *= expr1
        expr2 *= -1

        assert isinstance(expr1, Expression)
        assert isinstance(expr2, Expression)
        assert expr1.raw == 16
        assert expr2.raw == 3

    def test_itruediv_operation(self):
        # Test creation
        expr1: Expression = Expression(expression=2)
        expr2: Expression = Expression(expression=1)

        # Test __itruediv__ method
        expr1 /= expr1
        expr2 /= -2

        assert isinstance(expr1, Expression)
        assert isinstance(expr2, Expression)
        assert expr1.raw == 1
        assert expr2.raw == -0.5

    def test_ifloordiv_operation(self):
        # Test creation
        expr1: Expression = Expression(expression=4.5)
        expr2: Expression = Expression(expression=-8)

        # Test __ifloordiv__ method
        expr1 //= expr1
        expr2 //= -2

        assert isinstance(expr1, Expression)
        assert isinstance(expr2, Expression)
        assert expr1.raw == 1
        assert expr2.raw == 4

    def test_imod_operation(self):
        # Test creation
        expr1: Expression = Expression(expression=9.8)
        expr2: Expression = Expression(expression=6.2)

        # Test __imod__ method
        expr1 %= expr1
        expr2 %= 2

        assert isinstance(expr1, Expression)
        assert isinstance(expr2, Expression)
        assert isclose(expr1.raw, 0)
        assert isclose(expr2.raw, 0.2)

    def test_ipow_operation(self):
        # Test creation
        expr1: Expression = Expression(expression=3)
        expr2: Expression = Expression(expression=2)

        # Test __ipow__ method
        expr1 **= expr1
        expr2 **= 2

        assert isinstance(expr1, Expression)
        assert isinstance(expr2, Expression)
        assert expr1.raw == 27
        assert expr2.raw == 4
