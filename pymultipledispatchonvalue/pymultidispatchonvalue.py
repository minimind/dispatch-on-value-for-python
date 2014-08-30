import itertools


class AnyValue:
    def __init__(self, num):
        self.num = num

any_a = AnyValue(1)
any_b = AnyValue(2)
any_c = AnyValue(3)
any_d = AnyValue(4)


def dispatch(fn, stream, pattern):
    (matched, matched_stream) = match(stream, pattern)
    if matched:
        fn(matched_stream)
        return True
    else:
        return False


def match(stream, pattern):
    return real_match(stream, pattern, {})


def real_match(stream, pattern, context):
    # Maybe it's any_x?
    if isinstance(pattern, AnyValue):
        if pattern.num in context:
            return context[pattern.num] == stream, stream
        else:
            context[pattern.num] = stream
            return True, stream

    # We'll assume it's callable
    try:
        return pattern(stream), stream

    except TypeError:
        if not type(stream) == type(pattern):
            return False, []

        # OK, we'll assume it's a dictionary
        try:
            return compare_dictionaries(stream, pattern, context)

        except AttributeError:
            # Maybe a string or a list?
            try:
                # I hate to add an isinstance here but I can't see 
                # how to lose it
                if isinstance(stream, basestring):
                    return compare_primitives(stream, pattern, context)
                else:
                    return compare_lists(stream, pattern, context)

            except TypeError:
                # Have to assume primitives
                return compare_primitives(stream, pattern, context)


def compare_primitives(stream, pattern, context):
    if type(stream) == type(pattern) and stream == pattern:
        return True, stream
    else:
        return False, []


def compare_lists(stream, pattern, context):
    # We compare each item in the list. If they all match, then we have
    # a match.
    if not len(stream) == len(pattern):
        return False, []

    for s, p in itertools.izip(stream, pattern):
        (matched, matched_stream) = real_match(s, p, context)
        if not matched:
            return False, []

    return True, stream


def compare_dictionaries(stream, pattern, context):
    for k, v in pattern.iteritems():
        if not k in stream:
            return False, []

        s = stream[k]
        (matched, matched_stream) = real_match(s, v, context)
        if not matched:
            return False, []

    return True, stream
