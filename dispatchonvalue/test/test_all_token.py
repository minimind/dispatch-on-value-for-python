import unittest
import dispatchonvalue as dv


class TestAllToken(unittest.TestCase):
    def setUp(self):
        self.dispatch_on_value = dv.DispatchOnValue()

    def test_all_token1(self):
        stream = [1]
        pattern = dv.all_match(1)
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {}, {}
        )
        assert matched
        assert stream_found == [1]

    def test_all_token2(self):
        stream = [1, 1]
        pattern = dv.all_match(1)
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {}, {}
        )
        assert matched
        assert stream_found == [1, 1]

    def test_all_token3(self):
        stream = [1, 2]
        pattern = dv.all_match(1)
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {}, {}
        )
        assert not matched

    def test_all_token4(self):
        stream = [1, 2]
        pattern = dv.all_match(2)
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {}, {}
        )
        assert not matched

    def test_all_token5(self):
        stream = [
            {'type': 'frog', 'name': 'sid'},
            {'name': 'sid', 'age': 32}
        ]

        pattern = dv.all_match({'name': 'sid'})
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {}, {}
        )
        assert matched
        assert stream_found == stream

    def test_all_token6(self):
        stream = [
            {'type': 'frog', 'name': 'sidney'},
            {'name': 'sid', 'age': 32}
        ]

        pattern = dv.all_match({'name': 'sid'})
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {}, {}
        )
        assert not matched

    def test_all_token7(self):
        stream = [
            {'type': 'frog', 'name': 'sid'},
            {'name': 'sid', 'age': 32}
        ]

        pattern = dv.all_match({'name': dv.any_a})
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {}, {}
        )
        assert matched
        assert stream_found == stream

    def test_all_token8(self):
        stream = [
            {'type': 'frog', 'name': 'sidney'},
            {'name': 'sid', 'age': 32}
        ]

        pattern = dv.all_match({'name': dv.any_a})
        (matched, stream_found) = self.dispatch_on_value._match(
            stream, pattern, {}, {}
        )
        assert not matched
