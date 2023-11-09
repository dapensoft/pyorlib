from math import isclose

from pyorlib.mp.common.enums import ValueType
from pyorlib.mp.math import Element
from pyorlib.mp.math.expressions import Expression
from pyorlib.mp.math.terms import Term
from pyorlib.mp.math.terms.constants import Constant


class TestTerm:

    def test_inheritance(self):
        assert issubclass(Term, Element)

    def test_iadd_operation(self):
        # Test creation
        term1: Term = Constant(name='c_1', value_type=ValueType.CONTINUOUS, value=3)
        term2: Term = Constant(name='c_2', value_type=ValueType.CONTINUOUS, value=9)

        # Test __iadd__ method
        term1 += term1
        term2 += 3

        assert isinstance(term1, Expression)
        assert isinstance(term2, Expression)
        assert term1.raw == 6
        assert term2.raw == 12

    def test_isub_operation(self):
        # Test creation
        term1: Term = Constant(name='c_1', value_type=ValueType.CONTINUOUS, value=2)
        term2: Term = Constant(name='c_2', value_type=ValueType.CONTINUOUS, value=-11)

        # Test __isub__ method
        term1 -= term1
        term2 -= 5

        assert isinstance(term1, Expression)
        assert isinstance(term2, Expression)
        assert term1.raw == 0
        assert term2.raw == -16

    def test_imul_operation(self):
        # Test creation
        term1: Term = Constant(name='c_1', value_type=ValueType.CONTINUOUS, value=-4)
        term2: Term = Constant(name='c_2', value_type=ValueType.CONTINUOUS, value=-3)

        # Test __imul__ method
        term1 *= term1
        term2 *= -1

        assert isinstance(term1, Expression)
        assert isinstance(term2, Expression)
        assert term1.raw == 16
        assert term2.raw == 3

    def test_itruediv_operation(self):
        # Test creation
        term1: Term = Constant(name='c_1', value_type=ValueType.CONTINUOUS, value=2)
        term2: Term = Constant(name='c_2', value_type=ValueType.CONTINUOUS, value=1)

        # Test __itruediv__ method
        term1 /= term1
        term2 /= -2

        assert isinstance(term1, Expression)
        assert isinstance(term2, Expression)
        assert term1.raw == 1
        assert term2.raw == -0.5

    def test_ifloordiv_operation(self):
        # Test creation
        term1: Term = Constant(name='c_1', value_type=ValueType.CONTINUOUS, value=4.5)
        term2: Term = Constant(name='c_2', value_type=ValueType.CONTINUOUS, value=-8)

        # Test __ifloordiv__ method
        term1 //= term1
        term2 //= -2

        assert isinstance(term1, Expression)
        assert isinstance(term2, Expression)
        assert term1.raw == 1
        assert term2.raw == 4

    def test_imod_operation(self):
        # Test creation
        term1: Term = Constant(name='c_1', value_type=ValueType.CONTINUOUS, value=9.8)
        term2: Term = Constant(name='c_1', value_type=ValueType.CONTINUOUS, value=6.2)

        # Test __imod__ method
        term1 %= term1
        term2 %= 2

        assert isinstance(term1, Expression)
        assert isinstance(term2, Expression)
        assert isclose(term1.raw, 0)
        assert isclose(term2.raw, 0.2)

    def test_ipow_operation(self):
        # Test creation
        term1: Term = Constant(name='c_1', value_type=ValueType.CONTINUOUS, value=3)
        term2: Term = Constant(name='c_1', value_type=ValueType.CONTINUOUS, value=2)

        # Test __ipow__ method
        term1 **= term1
        term2 **= 2

        assert isinstance(term1, Expression)
        assert isinstance(term2, Expression)
        assert term1.raw == 27
        assert term2.raw == 4
