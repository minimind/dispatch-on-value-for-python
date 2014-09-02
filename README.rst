============================
Dispatch on Value for Python
============================

This package provides the ability to dispatch on values (as opposed to dispatch
on types) for nested lists, dictionaries, and primitive types (basically all
inbuilt types). You can use ``lambda`` to do expression matching and use a
wildcard to ensure identical values can be matched (see ``any_a``). It can
alleviate complicated and difficult to read ``if...elif...elif...`` chains and
greatly reduce the amount of code written.

Additionally, patterns can be registered dynamically, allowing a great flexibility
in which functions are called with which value.

The home page is on github at:

https://github.com/minimind/dispatch-on-value-for-python

Install using pip::

    pip install dispatchonvalue

Unit tests can be run from the source directory using::

    python -m unittest discover -s test

Any queries and comments are welcome. Send them to:

ian.macinnes@gmail.com

***********
Quick guide
***********

First you need to register your dispatch methods, also side the pattern they
should match on.

::

    import dispatchonvalue as dv

    dispatch_on_value = dv.DispatchOnValue()

    # Register your overloaded functions:
    @dispatch_on_value.add([1, 2, 3])  # [1, 2, 3] is the pattern to match on
    def _(a):
        assert a == [1, 2, 3]
        # Do something

    @dispatch_on_value.add([4, 5, 6])  # [4, 5, 6] is the pattern to match on
    def _(a):
        assert a == [4, 5, 6]
        # Do something

Then else where in your code, dispatch to the correct function based on the
value of the parameter passed::

    p = [4, 5, 6]
    dispatch_on_value.dispatch(p)  # Will call second function above

The return value is ``True`` or ``False``, depending upon whether a function
could be matched, dispatched, and called.

*******************
Some quick examples
*******************

Multiple dispatch on value
==========================

The simplest use is to dispatch on fixed values. Here we dispatch to two
different functions ``fn_1`` and ``fn_2`` depending upon the value of ``p``::

    @dispatch_on_value.add([1, 2, 3])
    def fn_1(a):
        assert a == [1, 2, 3]
        # Do something

    @dispatch_on_value.add([4, 5, 6])
    def fn_2(a):
        assert a == [4, 5, 6]
        # Do something

    p = [1, 2, 3]
    dispatch_on_value.dispatch(p)  # This will call fn_1 and return True

    p = [4, 5, 6]
    dispatch_on_value.dispatch(p)  # This will call fn_2 and return True

    p = [1, 2, 6]
    dispatch_on_value.dispatch(p)  # This will not call anything and return False

Data structure patterns can be arbitrary nested
===============================================

::

    @dispatch_on_value.add({'one': 3, 'animals': ['frog', 'mouse']})

Wildcards
=========

Use of wildcard tokens ``any_a``, ``any_b``, ... ``any_z`` that will ensure values are identical. e.g.::

    @dispatch_on_value.add([dv.any_a, 'b', 3, [3, 'd', dv.any_a]])
    def _(a):
        # Do something
    
    dispatch_on_value.dispatch(['c', 'b', 3, [3, 'd', 'c']])  # This will match
    dispatch_on_value.dispatch(['f', 'b', 3, [3, 'd', 'f']])  # This will match
    dispatch_on_value.dispatch(['c', 'b', 3, [3, 'd', 'f']])  # This will not match

Insert Lambda for wide expression of patterns 
=============================================

Use ``lambda``'s as part of the pattern matching::

   @dispatch_on_value.add([1, 2, lambda x: 3 < x < 7, 'hello'])
   def _(a):
       # Do something
    
   dispatch_on_value.dispatch([1, 2, 4, 'hello'])  # This will match
   dispatch_on_value.dispatch([1, 2, 2, 'hello'])  # This will not match

Another example::

   @dispatch_on_value.add(['a', 2, lambda x: x == 'b' or x == 'c'])
   def _(a):
       # Do something

   dispatch_on_value.dispatch(['a', 2, 'c'])  # This will match
   dispatch_on_value.dispatch(['a', 2, 's'])  # This will not match

No limit on parameters
======================

You can pass as many extra parameters as you want when dispatching::

    @dispatch_on_value.add([1, 2])
    def _(a, my_abc, my_def):
        assert a == [1, 2]
        # Do something
    
    dispatch_on_value.dispatch([1, 2], 'abc', 'def')

****************************************************
Matching on dictionaries is either partial or strict
****************************************************

Matching on directories is partial by default. This means dictionaries will
match if the key/value pairs in the pattern are matched - any extra pairs in
the value passed will be ignored. For example::

    @dispatch_on_value.add({'name': 'john', 'age': 32})
    def _(a):
        # Do something

    # These will match because they contain the minimal dictionary items
    dispatch_on_value.dispatch({'name': 'john', 'age': 32})
    dispatch_on_value.dispatch({'name': 'john', 'age': 32, 'sex': 'male'})

You can ensure dictionaries have to be exactly the same when matched by using
``dispatch_strict()`` rather than ``dispatch()``. For example::

    # This will match because it's strict and the pattern is exactly the same
    dispatch_on_value.dispatch_strict({'name': 'john', 'age': 32})

    # This will not match because the dictionary doesn't match exactly
    dispatch_on_value.dispatch_strict({'name': 'john', 'age': 32, 'sex': 'male'})
