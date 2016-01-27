"""Provide dispatch on value for complex arbitrarily nested lists and
dictionaries.

You can use lambda to do expression matching and an 'any' token that is a
wildcard that ensures identical values can be matched. It is useful for getting
rid of complicated and difficult to read if...elif...elif... chains.

"""
import six
from six.moves import zip
from functools import partial

class _AnyValue(object):
    """Allow wildcard item in DispatchOnValue."""
    def __init__(self, num):
        self.num = num

any_a = _AnyValue(1)
any_b = _AnyValue(2)
any_c = _AnyValue(3)
any_d = _AnyValue(4)
any_e = _AnyValue(5)
any_f = _AnyValue(6)
any_g = _AnyValue(7)
any_h = _AnyValue(8)
any_i = _AnyValue(9)
any_j = _AnyValue(10)
any_k = _AnyValue(11)
any_l = _AnyValue(12)
any_m = _AnyValue(13)
any_n = _AnyValue(14)
any_o = _AnyValue(15)
any_p = _AnyValue(16)
any_q = _AnyValue(17)
any_r = _AnyValue(18)
any_s = _AnyValue(19)
any_t = _AnyValue(20)
any_u = _AnyValue(21)
any_v = _AnyValue(22)
any_w = _AnyValue(23)
any_x = _AnyValue(24)
any_y = _AnyValue(25)
any_z = _AnyValue(26)


class AllValue(object):
    """Specify the entire iterable must match the single pattern"""
    def __init__(self, pattern):
        self.pattern = pattern


def all_match(p):
    return AllValue(p)


class DispatchFailed(Exception):
    pass


class DispatchOnValue(object):
    """Provide dispatch on value for complex arbitrarily nested lists and
    dictionaries."""

    def __init__(self):
        self.functions = []

    def add(self, pattern):
        """Decorator to add new dispatch functions."""
        def wrap(f):
            self.functions.append((f, pattern))
            return f

        return wrap

    def add_method(self, pattern):
        """Decorator to add new dispatch functions."""
        def wrap(f):
            def frozen_function(class_instance, f):
                def _(pattern):
                    return f(class_instance, pattern)

                return _

            self.functions.append((frozen_function(self, f), pattern))
            return f

        return wrap

    def dispatch(self, stream, *args, **kwargs):
        """
        Dispatch to function held internally depending upon the value of stream.

        Matching on directories is partial. This means dictionaries will
        match if all the key/value pairs in the pattern are matched - any extra
        pairs will be ignored.

        """
        for f, pat in self.functions:
            matched, matched_stream = self._match(stream, pat, {}, {})
            if matched:
                return f(matched_stream, *args, **kwargs)

        raise DispatchFailed()

    def dispatch_strict(self, stream, *args, **kwargs):
        """
        Dispatch to function held internally depending upon the value of stream.

        Matching on directories is strict. This means dictionaries will
        match if they are exactly the same.

        """
        for f, pat in self.functions:
            matched, matched_stream = self._match(stream, pat, 
                                                  {'strict': True}, {})
            if matched:
                return f(matched_stream, *args, **kwargs)

        raise DispatchFailed()

    def _match(self, stream, pattern, context, any_values):
        if isinstance(pattern, _AnyValue):
            if pattern.num in any_values:
                return any_values[pattern.num] == stream, stream
            else:
                any_values[pattern.num] = stream
                return True, stream

        try:
            if isinstance(pattern, AllValue):
                new_context = context.copy()
                new_context['single_pattern'] = True
                return self._compare_lists(stream, pattern.pattern,
                                           new_context, any_values)

            # Is it callable?
            return pattern(stream), stream

        except TypeError:
            if type(stream) != type(pattern):
                return False, []

            try:
                # OK, we'll assume it's a dictionary
                return self._compare_dictionaries(stream, pattern,
                                                  context, any_values)

            except (AttributeError, TypeError):
                # Maybe a string or a list?
                try:
                    # I hate to add an isinstance() here but I can't see
                    # how to lose it
                    if isinstance(stream, six.string_types):
                        return self._compare_primitives(stream, pattern)
                    else:
                        return self._compare_lists(stream, pattern,
                                                   context, any_values)

                except TypeError:
                    # Have to assume primitives
                    return self._compare_primitives(stream, pattern)

    @staticmethod
    def _compare_primitives(stream, pattern):
        if type(stream) == type(pattern) and stream == pattern:
            return True, stream
        else:
            return False, []

    def _compare_lists(self, stream, pattern, context, any_values):
        # We compare each item in the list. If they all match, then we have
        # a match.
        if 'single_pattern' in context and context['single_pattern']:
            for s in stream:
                new_context = context.copy()
                del new_context['single_pattern']
                (matched, matched_stream) = self._match(s, pattern,
                                                        new_context, any_values)
                if not matched:
                    return False, []
        else:
            if len(stream) != len(pattern):
                return False, []

            for s, p in zip(stream, pattern):
                (matched, matched_stream) = self._match(s, p, context,
                                                        any_values)
                if not matched:
                    return False, []

        return True, stream

    def _compare_dictionaries(self, stream, pattern, context, any_values):
        if 'strict' in context and context['strict']:
            if len(stream) != len(pattern):
                return False, []

        for k, v in six.iteritems(pattern):
            if not k in stream:
                return False, []

            s = stream[k]
            (matched, matched_stream) = self._match(s, v, context, any_values)
            if not matched:
                return False, []

        return True, stream
