import unittest
import pymultidispatchonvalue


class TestSequenceFunctions(unittest.TestCase):

    '''def test_shuffle(self):
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
        assert ran_fn1'''

    def test_primitive1(self):
        stream = 3
        pattern = 3
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_primitive2(self):
        stream = 3
        pattern = 4
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_primitive3(self):
        stream = 3
        pattern = '3'
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_primitive4(self):
        stream = '3km'
        pattern = '3km'
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_list1(self):
        stream = [4]
        pattern = [4]
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_list2(self):
        stream = [4]
        pattern = [5]
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_list3(self):
        stream = [4, 5]
        pattern = [4, 5]
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_list4(self):
        stream = [4, 5]
        pattern = [4, 6]
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_list5(self):
        stream = [4, 5, [6, 7]]
        pattern = [4, 5, [6, 7]]
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_list6(self):
        stream = [4, 5, [6, 7]]
        pattern = [4, 5, [6, 8]]
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_tuple1(self):
        stream = (1,2)
        pattern = (1,2)
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_tuple2(self):
        stream = (1,2)
        pattern = (1,3)
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_tuple3(self):
        stream = (1,2)
        pattern = (1,2,3)
        matched = pymultidispatchonvalue.match(stream, pattern)
        assert not matched



if __name__ == '__main__':
    unittest.main()
