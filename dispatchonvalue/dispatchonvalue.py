"""Provide dispatch on value for complex arbitrarily nested lists and
dictionaries.

You can use lambda to do expression matching and an 'any' token that is a
wildcard that ensures identical values can be matched. It is useful for getting
rid of complicated and difficult to read if...elif...elif... chains.

"""
import six
from six.moves import zip


class AnyValue(object):
    """Allow wildcard item in DispatchOnValue."""
    def __init__(self, num):
        self.num = num

any_a = AnyValue(1)
any_b = AnyValue(2)
any_c = AnyValue(3)
any_d = AnyValue(4)
any_e = AnyValue(5)
any_f = AnyValue(6)
any_g = AnyValue(7)
any_h = AnyValue(8)
any_i = AnyValue(9)
any_j = AnyValue(10)
any_k = AnyValue(11)
any_l = AnyValue(12)
any_m = AnyValue(13)
any_n = AnyValue(14)
any_o = AnyValue(15)
any_p = AnyValue(16)
any_q = AnyValue(17)
any_r = AnyValue(18)
any_s = AnyValue(19)
any_t = AnyValue(20)
any_u = AnyValue(21)
any_v = AnyValue(22)
any_w = AnyValue(23)
any_x = AnyValue(24)
any_y = AnyValue(25)
any_z = AnyValue(26)


class AllValue(object):
    """Specify the entire iterable must match the single pattern"""
    def __init__(self, pattern):
        self.pattern = pattern


def all_match(p):
    return AllValue(p)

class DispatchOnValue(object):
    """Provide dispatch on value for complex arbitrarily nested lists and
    dictionaries."""

    def __init__(self):
        self.functions = []

    def add(self, pattern):
        """Decorator to add new dispatch functions."""
        self_of_parent = self

        def wrap(f):
            def wrapped_f(*args):
                f(*args)

            self_of_parent.functions.append((f, pattern))
            return wrapped_f

        return wrap

    def dispatch(self, stream, *args):
        """
        Dispatch to function held internally depending upon the value of stream.

        Matching on directories is partial. This means dictionaries will
        match if all the key/value pairs in the pattern are matched - any extra
        pairs will be ignored.

        """
        for t in self.functions:
            (matched, matched_stream) = self._match(
                stream, t[1], {}, {}
            )
            if matched:
                f = t[0]
                f(matched_stream, *args)
                return True

        return False

    def dispatch_strict(self, stream, *args):
        """
        Dispatch to function held internally depending upon the value of stream.

        Matching on directories is strict. This means dictionaries will
        match if they are exactly the same.

        """
        for t in self.functions:
            (matched, matched_stream) = self._match(
                stream, t[1], {'strict': True}, {}
            )
            if matched:
                f = t[0]
                f(matched_stream, *args)
                return True

        return False

    def _match(self, stream, pattern, context, any_values):
        if isinstance(pattern, AnyValue):
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
            if not type(stream) == type(pattern):
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
            if not len(stream) == len(pattern):
                return False, []

            for s, p in zip(stream, pattern):
                (matched, matched_stream) = self._match(s, p, context,
                                                        any_values)
                if not matched:
                    return False, []

        return True, stream

    def _compare_dictionaries(self, stream, pattern, context, any_values):
        if 'strict' in context and context['strict']:
            if not len(stream) == len(pattern):
                return False, []

        for k, v in six.iteritems(pattern):
            if not k in stream:
                return False, []

            s = stream[k]
            (matched, matched_stream) = self._match(s, v, context, any_values)
            if not matched:
                return False, []

        return True, stream
