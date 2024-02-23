from math import isclose

from pyorlib.algebra import Element, Expression


class TestElement:

    def test_add_and_radd_operation(self):
        # Test creation
        expr1: Element = Expression(expression=3)
        expr2: Element = Expression(expression=9)

        assert expr1.raw == 3 and expr2.raw == 9

        # Test __add__ method between expressions
        expr3 = expr1 + expr2
        expr4 = expr2 + expr1

        assert isinstance(expr3, Element)
        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr3)
        assert id(expr2) != id(expr4)
        assert expr3.raw == 12
        assert expr4.raw == 12

        # Test __add__ & __radd__ method between number and expressions
        expr5 = expr2 + 2
        expr6 = 1 + expr1
        expr7 = expr5.__radd__(expr6)

        assert isinstance(expr5, Element)
        assert isinstance(expr6, Element)
        assert isinstance(expr7, Element)
        assert id(expr1) != id(expr5)
        assert id(expr2) != id(expr6)
        assert id(expr5) != id(expr7)
        assert expr5.raw == 11
        assert expr6.raw == 4
        assert expr7.raw == 15

        # Test __iadd__ method
        expr1 += expr1
        expr2 += 3

        assert expr1.raw == 6
        assert expr2.raw == 12

    def test_sub_and_rsub_operation(self):
        # Test creation
        expr1: Element = Expression(expression=2)
        expr2: Element = Expression(expression=-11)

        assert expr1.raw == 2 and expr2.raw == -11

        # Test __sub__ method between expressions
        expr3 = expr1 - expr2
        expr4 = expr2 - expr1

        assert isinstance(expr3, Element)
        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr3)
        assert id(expr2) != id(expr4)
        assert expr3.raw == 13
        assert expr4.raw == -13

        # Test __sub__ & __rsub__ method between number and expressions
        expr5 = expr1 - 3
        expr6 = 2 - expr2
        expr7 = expr5.__rsub__(expr6)

        assert isinstance(expr5, Element)
        assert isinstance(expr6, Element)
        assert isinstance(expr7, Element)
        assert id(expr1) != id(expr5)
        assert id(expr2) != id(expr6)
        assert id(expr5) != id(expr7)
        assert expr5.raw == -1
        assert expr6.raw == 13
        assert expr7.raw == 14

    def test_mul_and_rmul_operation(self):
        # Test creation
        expr1: Element = Expression(expression=-4)
        expr2: Element = Expression(expression=-3)

        assert expr1.raw == -4 and expr2.raw == -3

        # Test __mul__ method between expressions
        expr3 = expr1 * expr2
        expr4 = expr2 * expr1

        assert isinstance(expr3, Element)
        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr3)
        assert id(expr2) != id(expr4)
        assert expr3.raw == 12
        assert expr4.raw == 12

        # Test __mul__ & __rmul__ method between number and expressions
        expr5 = expr1 * 2
        expr6 = -2 * expr2
        expr7 = expr5.__rmul__(expr6)

        assert isinstance(expr5, Element)
        assert isinstance(expr6, Element)
        assert isinstance(expr7, Element)
        assert id(expr1) != id(expr5)
        assert id(expr2) != id(expr6)
        assert id(expr5) != id(expr7)
        assert expr5.raw == -8
        assert expr6.raw == 6
        assert expr7.raw == -48

    def test_truediv_and_rtruediv_operation(self):
        # Test creation
        expr1: Element = Expression(expression=2)
        expr2: Element = Expression(expression=1)

        assert expr1.raw == 2 and expr2.raw == 1

        # Test __truediv__ method between expressions
        expr3 = expr1 / expr2
        expr4 = expr2 / expr1

        assert isinstance(expr3, Element)
        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr3)
        assert id(expr2) != id(expr4)
        assert expr3.raw == 2
        assert expr4.raw == 0.5

        # Test __truediv__ & __rtruediv__ method between number and expressions
        expr5 = expr1 / -2
        expr6 = 2 / expr2
        expr7 = expr5.__rtruediv__(expr6)

        assert isinstance(expr5, Element)
        assert isinstance(expr6, Element)
        assert isinstance(expr7, Element)
        assert id(expr1) != id(expr5)
        assert id(expr2) != id(expr6)
        assert id(expr5) != id(expr7)
        assert expr5.raw == -1
        assert expr6.raw == 2
        assert expr7.raw == -2

    def test_floordiv_and_rfloordiv_operation(self):
        # Test creation
        expr1: Element = Expression(expression=4.5)
        expr2: Element = Expression(expression=-8)

        assert expr1.raw == 4.5 and expr2.raw == -8

        # Test __floordiv__ method between expressions
        expr3 = expr1 // expr2
        expr4 = expr2 // expr1

        assert isinstance(expr3, Element)
        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr3)
        assert id(expr2) != id(expr4)
        assert expr3.raw == -1
        assert expr4.raw == -2

        # Test __floordiv__ & __rfloordiv__ method between number and expressions
        expr5 = expr1 // -2
        expr6 = 2 // expr2
        expr7 = expr5.__rfloordiv__(expr6)

        assert isinstance(expr5, Element)
        assert isinstance(expr6, Element)
        assert isinstance(expr7, Element)
        assert id(expr1) != id(expr5)
        assert id(expr2) != id(expr6)
        assert id(expr5) != id(expr7)
        assert expr5.raw == -3
        assert expr6.raw == -1
        assert expr7.raw == 0

    def test_mod_and_rmod_operation(self):
        # Test creation
        expr1: Element = Expression(expression=9.8)
        expr2: Element = Expression(expression=6.2)

        assert expr1.raw == 9.8 and expr2.raw == 6.2

        # Test __mod__ method between expressions
        expr3 = expr1 % expr2
        expr4 = expr2 % expr1

        assert isinstance(expr3, Element)
        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr3)
        assert id(expr2) != id(expr4)
        assert isclose(expr3.raw, 3.6)
        assert isclose(expr4.raw, 6.2)

        # Test __mod__ & __rmod__ method between number and expressions
        expr5 = expr1 % 2
        expr6 = 2 % expr2
        expr7 = expr5.__rmod__(expr6)

        assert isinstance(expr5, Element)
        assert isinstance(expr6, Element)
        assert isinstance(expr7, Element)
        assert id(expr1) != id(expr5)
        assert id(expr2) != id(expr6)
        assert id(expr5) != id(expr7)
        assert isclose(expr5.raw, 1.8)
        assert isclose(expr6.raw, 2)
        assert isclose(expr7.raw, 0.2)

    def test_pow_and_rpow_operation(self):
        # Test creation
        expr1: Element = Expression(expression=3)
        expr2: Element = Expression(expression=2)

        assert expr1.raw == 3 and expr2.raw == 2

        # Test __pow__ method between expressions
        expr3 = expr1**expr2
        expr4 = expr2**expr1

        assert isinstance(expr3, Element)
        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr3)
        assert id(expr2) != id(expr4)
        assert expr3.raw == 9
        assert expr4.raw == 8

        # Test __pow__ & __rpow__ method between number and expressions
        expr5 = expr1**2
        expr6 = 2**expr2
        expr7 = expr5.__rpow__(expr6)

        assert isinstance(expr5, Element)
        assert isinstance(expr6, Element)
        assert isinstance(expr7, Element)
        assert id(expr1) != id(expr5)
        assert id(expr2) != id(expr6)
        assert id(expr5) != id(expr7)
        assert expr5.raw == 9
        assert expr6.raw == 4
        assert expr7.raw == 262144

    def test_ne_operation(self):
        # Test creation
        expr1: Element = Expression(expression=3)

        assert expr1.raw == 3

        # Test __neg__ method
        expr2 = -expr1

        assert isinstance(expr2, Element)
        assert id(expr1) != id(expr2)
        assert expr2.raw == -3

    def test_pos_operation(self):
        # Test creation
        expr1: Element = Expression(expression=-3)

        assert expr1.raw == -3

        # Test __pos__ method
        expr2 = +expr1

        assert isinstance(expr2, Element)
        assert id(expr1) != id(expr2)
        assert expr2.raw == -3

    def test_abs_operation(self):
        # Test creation
        expr1: Element = Expression(expression=-3)

        assert expr1.raw == -3

        # Test __abs__ method
        expr2 = abs(expr1)

        assert isinstance(expr2, Element)
        assert id(expr1) != id(expr2)
        assert expr2.raw == 3

    def test_eq_comparison(self):
        # Test creation
        expr1: Element = Expression(expression=6)
        expr2: Element = Expression(expression=7)

        assert expr1.raw == 6 and expr2.raw == 7

        # Test __eq__ method between expressions
        expr3 = expr1 == expr2

        assert isinstance(expr3, Element)
        assert id(expr1) != id(expr3)
        assert not expr3.raw

        # Test __eq__ method between number and expressions
        expr4 = expr2 == 7

        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr4)
        assert expr4.raw

    def test_ne_comparison(self):
        # Test creation
        expr1: Element = Expression(expression=7)
        expr2: Element = Expression(expression=8)

        assert expr1.raw == 7 and expr2.raw == 8

        # Test __ne__ method between expressions
        expr3 = expr1 != expr2

        assert isinstance(expr3, Element)
        assert id(expr1) != id(expr3)
        assert expr3.raw

        # Test __ne__ method between number and expressions
        expr4 = expr2 != 8

        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr4)
        assert not expr4.raw

    def test_lt_comparison(self):
        # Test creation
        expr1: Element = Expression(expression=8)
        expr2: Element = Expression(expression=9.1)

        assert expr1.raw == 8 and expr2.raw == 9.1

        # Test __lt__ method between expressions
        expr3 = expr1 < expr2

        assert isinstance(expr3, Element)
        assert id(expr1) != id(expr3)
        assert expr3.raw

        # Test __lt__ method between number and expressions
        expr4 = expr1 < 8

        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr4)
        assert not expr4.raw

    def test_le_comparison(self):
        # Test creation
        expr1: Element = Expression(expression=9.4)
        expr2: Element = Expression(expression=10.3)

        assert expr1.raw == 9.4 and expr2.raw == 10.3

        # Test __le__ method between expressions
        expr3 = expr1 <= expr2

        assert isinstance(expr3, Element)
        assert id(expr1) != id(expr3)
        assert expr3.raw

        # Test __le__ method between number and expressions
        expr4 = expr1 <= 9.39

        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr4)
        assert not expr4.raw

    def test_gt_comparison(self):
        # Test creation
        expr1: Element = Expression(expression=6)
        expr2: Element = Expression(expression=9)

        assert expr1.raw == 6 and expr2.raw == 9

        # Test __gt__ method between expressions
        expr3 = expr1 > expr2

        assert isinstance(expr3, Element)
        assert id(expr1) != id(expr3)
        assert not expr3.raw

        # Test __gt__ method between number and expressions
        expr4 = expr1 > 5

        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr4)
        assert expr4.raw

    def test_ge_comparison(self):
        # Test creation
        expr1: Element = Expression(expression=7)
        expr2: Element = Expression(expression=10)

        assert expr1.raw == 7 and expr2.raw == 10

        # Test __ge__ method between expressions
        expr3 = expr1 >= expr2

        assert isinstance(expr3, Element)
        assert id(expr1) != id(expr3)
        assert not expr3.raw

        # Test __ge__ method between number and expressions
        expr4 = expr1 >= 7

        assert isinstance(expr4, Element)
        assert id(expr1) != id(expr4)
        assert expr4.raw
