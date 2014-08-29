import unittest
import pymultidispatchonvalue

class TestSequenceFunctions(unittest.TestCase):

    def test_shuffle(self):
        ran_fn1 = False

        def fn1(li, a):
            ran_fn1 = True
            assert a == {'name': 'john', 'age': 32}

        dict1 = {'name': 'john', 'age': 32}

        (matched, tail) = pymultidispatchonvalue.match(
            dict1, fn1, [],
            {
                'name': 'john', 'age': 32
            }
        )

        assert matched
        assert ran_fn1

if __name__ == '__main__':
    unittest.main()
