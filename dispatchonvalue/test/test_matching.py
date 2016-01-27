import unittest
from .. import dispatchonvalue as dv


class TestMatching(unittest.TestCase):
    def setUp(self):
        self.dispatch_on_value = dv.DispatchOnValue()

    def test_primitive1(self):
        stream = 3
        pattern = 3
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_primitive2(self):
        stream = 3
        pattern = 4
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_primitive3(self):
        stream = 3
        pattern = '3'
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_primitive4(self):
        stream = '3km'
        pattern = '3km'
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_list1(self):
        stream = [4]
        pattern = [4]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_list2(self):
        stream = [4]
        pattern = [5]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_list3(self):
        stream = [4, 5]
        pattern = [4, 5]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_list4(self):
        stream = [4, 5]
        pattern = [4, 6]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_list5(self):
        stream = [4, 5, [6, 7]]
        pattern = [4, 5, [6, 7]]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_list6(self):
        stream = [4, 5, [6, 7]]
        pattern = [4, 5, [6, 8]]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_tuple1(self):
        stream = (1, 2)
        pattern = (1, 2)
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_tuple2(self):
        stream = (1, 2)
        pattern = (1, 3)
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_tuple3(self):
        stream = (1, 2)
        pattern = (1, 2, 3)
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_lambda1(self):
        stream = 1
        pattern = lambda x: x == 1
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_lambda2(self):
        stream = 3
        pattern = lambda x: 1 < x < 5
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_lambda3(self):
        stream = 7
        pattern = lambda x: 1 < x < 5
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_lambda4(self):
        stream = [1, 2, 3]
        pattern = [1, 2, lambda x: x == 3]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_lambda5(self):
        stream = [1, 2, 4]
        pattern = [1, 2, lambda x: x == 3]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_lambda6(self):
        stream = [1, 2, [4, 5]]
        pattern = [1, 2, [lambda x: x == 4, 5]]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_lambda7(self):
        stream = [1, 2, [4, 5]]
        pattern = [1, 2, [lambda x: x == 4, 4]]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_dict1(self):
        stream = {'one': 1}
        pattern = {'one': 1}
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_dict2(self):
        stream = {'one': 1, 'two': 2}
        pattern = {'one': 1, 'two': 2}
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_dict3(self):
        stream = {'one': 1, 'two': 3}
        pattern = {'one': 1, 'two': 2}
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_dict4(self):
        stream = {'one': 1, 'two': 2}
        pattern = {'one': 1}
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_dict5(self):
        stream = {'one': 1}
        pattern = {'one': 1, 'two': 2}
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_dict6(self):
        stream = {'one': 1, 'list': [1, 2]}
        pattern = {'one': 1, 'list': [1, 2]}
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_dict7(self):
        stream = {'one': 1, 'list': [1, 2]}
        pattern = {'one': 1, 'list': [1, 3]}
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_dict8(self):
        stream = {'one': 1, 'num': 6}
        pattern = {'one': 1, 'num': lambda x: 3 < x < 9}
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_dict9(self):
        stream = {'one': 1, 'num': 10}
        pattern = {'one': 1, 'num': lambda x: 3 < x < 9}
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_any1(self):
        stream = 1
        pattern = dv.any_a
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_any2(self):
        stream = 2
        pattern = dv.any_a
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_any3(self):
        stream = [1, 2]
        pattern = [dv.any_a, 2]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_any4(self):
        stream = [1, 2, 1]
        pattern = [dv.any_a, 2, dv.any_a]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_any5(self):
        stream = [1, 2, 2]
        pattern = [dv.any_a, 2, dv.any_a]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_any6(self):
        stream = [1, 2, 3, [1, 4, 5]]
        pattern = [dv.any_a, 2, 3, [dv.any_a, 4, 5]]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_any7(self):
        stream = [1, 2, 3, [2, 4, 5]]
        pattern = [dv.any_a, 2, 3, [dv.any_a, 4, 5]]
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_any8(self):
        stream = {'a': 1, 'b': 2, 'c': {'d': 2, 'e': 3}}
        pattern = {'a': 1, 'b': dv.any_b,
                   'c': {'e': 3, 'd': dv.any_b}}
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert matched
        assert stream == stream_found

    def test_any9(self):
        stream = {'a': 1, 'b': 2, 'c': {'d': 3, 'e': 3}}
        pattern = {'a': 1, 'b': dv.any_b,
                   'c': {'e': 3, 'd': dv.any_b}}
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched

    def test_any10(self):
        stream = {'a': 1, 'c': {'d': 2, 'e': 3}}
        pattern = {'a': 1, 'b': dv.any_b,
                   'c': {'e': 3, 'd': dv.any_b}}
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {'strict': False}, {}
        )
        assert not matched


if __name__ == '__main__':
    unittest.main()
