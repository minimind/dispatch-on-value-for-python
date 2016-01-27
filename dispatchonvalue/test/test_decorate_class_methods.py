import unittest
from .. import dispatchonvalue as dv


class TestDecorateClassMethod(unittest.TestCase):

    def test_decorate_class_method(self):
        dispatch_on_value = dv.DispatchOnValue()

        class MyClass(object):
            @dispatch_on_value.add_method([1, 2, 3])
            def m1(self, a):
                called[0] = 1
                return 2

            @dispatch_on_value.add_method([4, 5, 6])
            def m2(self, a):
                called[0] = 2
                return 3

        my_class = MyClass()

        called = [0]

        p = [4, 5, 6]
        # Should call second function above
        assert dispatch_on_value.dispatch(p) == 3
        assert called[0] == 2
