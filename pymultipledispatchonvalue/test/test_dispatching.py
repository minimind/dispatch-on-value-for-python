import unittest
from pymultidispatchonvalue import *


class TestBasicMatching(unittest.TestCase):
    def test_dispatch1(self):
        dispatchOnValue = DispatchOnValue()

        @dispatchOnValue.add(1)
        def _(a, s):
            print 'matched 1 - parameters is ' + s

        @dispatchOnValue.add(2)
        def _(a):
            print 'matched 2 - ' + str(a)

        # What about additional parameters...?
        dispatchOnValue.dispatch(1, 'hello')
        dispatchOnValue.dispatch(2)
