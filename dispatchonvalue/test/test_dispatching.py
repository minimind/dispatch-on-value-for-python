import unittest
import dispatchonvalue as dv


class TestBasicDispatching(unittest.TestCase):
    def test_dispatch1(self):
        dispatch_on_value = dv.DispatchOnValue()

        @dispatch_on_value.add(1)
        def _(a, s):
            print 'matched 1 - parameters is ' + s

        @dispatch_on_value.add(2)
        def _(a):
            print 'matched 2 - ' + str(a)

        # What about additional parameters...?
        dispatch_on_value.dispatch(1, 'hello')
        dispatch_on_value.dispatch(2)
