primitive_types = {int, float, str, bool}


def match(stream, fn1, d, pattern):
    if type(stream) in primitive_types:
        return compare_primitive(stream, pattern)

    elif type(pattern) is list:
        return compare_lists(stream, pattern)


def compare_primitive(stream, pattern):
    assert type(stream) in primitive_types

    if type(stream) == type(pattern) and stream == pattern:
        return True
    else:
        return False


def compare_lists(stream, pattern):
    # We compare each item in the list. If they all match, then we have
    # a match.
    if not len(stream) == len(pattern):
        return False, []

    for s, p in zip(stream, pattern):
        if type(p) in primitive_types:
            matched = compare_primitive(s, p)
            if not matched:
                return False

        elif type(p) is list:
            matched = compare_lists(s, p)
            if not matched:
                return False

    return True






def compare_dictionaries(stream, pattern):
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

    return True, stream

