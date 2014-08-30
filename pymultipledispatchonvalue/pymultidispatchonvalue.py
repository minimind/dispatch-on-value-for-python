import itertools


def match(stream, pattern):
    if not type(stream) == type(pattern):
        return False

    # We'll assume it's a dictionary
    try:
        raise AttributeError()  # return compare_dictionaries(stream, pattern)
    except AttributeError:
        # Maybe a list?
        try:
            if isinstance(stream, basestring):
                return compare_primitives(stream, pattern)
            else:
                return compare_lists(stream, pattern)

        except TypeError:
            # Have to assume primitives
            return compare_primitives(stream, pattern)


def compare_primitives(stream, pattern):
    if type(stream) == type(pattern) and stream == pattern:
        return True
    else:
        return False


def compare_lists(stream, pattern):
    # We compare each item in the list. If they all match, then we have
    # a match.
    if not len(stream) == len(pattern):
        return False

    for s, p in itertools.izip(stream, pattern):
        matched = match(s, p)
        if not matched:
            return False

    return True


'''def compare_dictionaries(stream, pattern):
    for k, v in pattern.iteritems():
        if not k in stream:
            return False, []

        v2 = stream[k]
        if type(v) in primitive_types and type(v) == type(v2):
            if not v == v2:
                return False, []

        elif type(v) is dict and type(v2) is dict:
            return compare_dictionaries(v, v2), stream

        elif type(v) is list and type(v2) is list:
            return compare_lists(v, v2), stream

    return True, stream'''

