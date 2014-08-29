primitive_types = {int, float, str, bool}


def match(stream, fn1, d, pattern):
    if type(stream) in primitive_types and type(stream) == type(pattern):
            if not stream == pattern:
                return False, []

    if type(pattern) is dict:
        if not type(stream) is dict:
            return False, []

        (matched, tail) = compare_dictionaries(stream, pattern)
        if not matched:
            return False, []

    elif type(pattern) is list:
        if not type(stream) is list:
            return False, []

        (matched, tail) = compare_lists(stream, pattern)
        if not matched:
            return False, []


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


def compare_lists(stream, pattern):
    if not len(stream) == len(pattern):
        return False, []

    for v, v2 in zip(pattern, stream):
        if type(v) in primitive_types and type(v) == type(v2):
            if not v == v2:
                return False, []

        elif type(v) is dict and type(v2) is dict:
            return compare_dictionaries(v, v2)

        elif type(v) is list and type(v2) is list:
            return compare_lists(v, v2)

    return True, stream
