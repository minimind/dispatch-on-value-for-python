============================
Dispatch on Value for Python
============================

This package provides  dispatch on value complex nested lists and dictionaries.
You can use lambda to do expression matching and an 'any' token that is a
wildcard that ensures identical values can be matched.

The home page is on github at:

https://github.com/minimind/dispatch-on-value-for-python

Unit tests can be run using::

    python -m unittest discover -s test

***********
Quick guide
***********

Start your code with this::

    import dispatchonvalue as dv

    dispatchOnValue = dv.DispatchOnValue()

Then register your overloaded functions::

    @dispatchOnValue.add([1, 2, 3])  # Primitive type value 1 is the matching pattern
    def _(a):
        assert a == 1
        # Do something

    @dispatchOnValue.add([4, 5, 6])  # Primitive type value 2 is the matching pattern
    def _(a):
        assert a == 2
        # Do something

Then later, call the correct overloaded functions::

    p = [4, 5, 6]
    dispatchOnValue.dispatch(p)  # Will call second function above

The return value is True or False, depending upon whether a function
could be matched and called.

*******************
Some quick examples
*******************

1. Multiple dispatch on value::

        @dispatchOnValue.add([1, 2, 3])
        def fn_1(a):
            assert a = [1, 2, 3]
            # Do something
    
        @dispatchOnValue.add([4, 5, 6])
        def fn_2(a):
            assert a = [4, 5, 6]
            # Do something
    
        p = [1, 2, 3]
        dispatchOnValue.dispatch(p)  # This will call fn_1 and return True
    
        p = [4, 5, 6]
        dispatchOnValue.dispatch(p)  # This will call fn_2 and return True
    
        p = [1, 2, 6]
        dispatchOnValue.dispatch(p)  # This will not call anything and return False

2.  Data structure patterns can be arbitrary nested::

        @dispatchOnValue.add({'one': 3, 'animals': ['frog', 'mouse']})

3. Use of wildcard tokens any_a, any_b, ... any_z that will ensure
values are identical. e.g.::

    @dispatchOnValue.add(['z', 'b', 3, [3, 'd', 'z']])
    def _(a):
        assert a == ['z', 'b', 3, [3, 'd', 'z']]
        # Do something
        
    dispatchOnValue.dispatch([any_a, 'b',   3, [3, 'd', any_a]])  # This will match
    dispatchOnValue.dispatch([any_a, any_a, 3, [3, 'd', any_a]])  # This will not match

4. You can pass as many extra parameters as you want when dispatching::

    @dispatchOnValue.add([1, 2])  # This is the matching pattern
    def _(a, my_abc, my_def):
        assert a == [1, 2]
        # Do something
    
    dispatchOnValue.dispatch([1, 2], 'abc', 'def')

5. Use lambda's as part of the pattern matching::

       @dispatchOnValue.add([1, 2, lambda x: 3 < x < 7, 'hello'])
       def _(a):
           # Do something
        
       dispatchOnValue.dispatch([1, 2, 4, 'hello'])  # This will match
       dispatchOnValue.dispatch([1, 2, 2, 'hello'])  # This will not match

   Another example::

       @dispatchOnValue.add(['a', 2, lambda x: x == 'b' or x == 'c'])
       def _(a):
           # Do something

       dispatchOnValue.dispatch(['a', 2, 'c'])  # This will match
       dispatchOnValue.dispatch(['a', 2, 's'])  # This will not match

****************************************************
Matching on dictionaries is either partial or strict
****************************************************

Matching on directories is partial by default. This means dictionaries will
match if all the key/value pairs in the pattern are matched - any extra pairs
will be ignored. You can ensure the dictionaries are exactly the same by using
dispatch_strict() rather than dispatch(). For example::

    @dispatchOnValue.add({'name': 'john', 'age': 32})
    def _(a):
        # Do something

    dict1 = {'name': 'john', 'age': 32}

    # These will match because they contain the minimal dictionary items
    dispatchOnValue.dispatch({'name': 'john', 'age': 32})
    dispatchOnValue.dispatch({'name': 'john', 'age': 32, 'sex': 'male'})

    # This will match because it's strict and the pattern is exactly the same
    dispatchOnValue.dispatch_strict({'name': 'john', 'age': 32})

    # This will not match because the dictionary doesn't match exactly
    dispatchOnValue.dispatch_strict({'name': 'john', 'age': 32, 'sex': 'male'})
