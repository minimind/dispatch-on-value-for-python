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
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert matched
        assert stream == stream_found

    def test_primitive2(self):
        stream = 3
        pattern = 4
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_primitive3(self):
        stream = 3
        pattern = '3'
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_primitive4(self):
        stream = '3km'
        pattern = '3km'
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_list1(self):
        stream = [4]
        pattern = [4]
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_list2(self):
        stream = [4]
        pattern = [5]
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_list3(self):
        stream = [4, 5]
        pattern = [4, 5]
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_list4(self):
        stream = [4, 5]
        pattern = [4, 6]
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_list5(self):
        stream = [4, 5, [6, 7]]
        pattern = [4, 5, [6, 7]]
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_list6(self):
        stream = [4, 5, [6, 7]]
        pattern = [4, 5, [6, 8]]
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_tuple1(self):
        stream = (1,2)
        pattern = (1,2)
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_tuple2(self):
        stream = (1,2)
        pattern = (1,3)
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_tuple3(self):
        stream = (1,2)
        pattern = (1,2,3)
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_lambda1(self):
        stream = 1
        pattern = lambda x: x == 1
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_lambda2(self):
        stream = 3
        pattern = lambda x: 1 < x < 5
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_lambda3(self):
        stream = 7
        pattern = lambda x: 1 < x < 5
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_lambda4(self):
        stream = [1, 2, 3]
        pattern = [1, 2, lambda x: x == 3]
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_lambda5(self):
        stream = [1, 2, 4]
        pattern = [1, 2, lambda x: x == 3]
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert not matched

    def test_lambda6(self):
        stream = [1, 2, [4, 5]]
        pattern = [1, 2, [lambda x: x == 4, 5]]
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert matched

    def test_lambda7(self):
        stream = [1, 2, [4, 5]]
        pattern = [1, 2, [lambda x: x == 4, 4]]
        (matched, stream_found) = pymultidispatchonvalue.match(stream, pattern)
        assert not matched


if __name__ == '__main__':
    unittest.main()
