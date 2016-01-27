============================
Dispatch on Value for Python
============================

This Python 2.7/Python 3.x package provides the ability to dispatch on values
(as opposed to dispatching on types) by pairing functions with patterns. It
uses pattern matching to dispatch on complex, nested data structures containing
lists, dictionaries and primitive types. You can use ``lambda`` to do
expression matching and utilise wildcard parameters to ensure identical values
can be matched (see ``any_a``). It can alleviate complicated and difficult to
read ``if ... elif ... elif ...`` chains and simplify the code.

Value patterns can be registered dynamically, allowing a great flexibility
in determining which functions are called on which value patterns.

The home page is on github at:

https://github.com/minimind/dispatch-on-value-for-python

Install using pip::

    pip install dispatchonvalue

Unit tests can be run from the source directory using::

    python -m unittest discover -s test

Any queries and comments are welcome. Send them to:

ian.macinnes@gmail.com

*****
Guide
*****

Very quick example
==================

First register your dispatch methods, alongside the pattern they should match on::

    import dispatchonvalue as dv

    dispatch_on_value = dv.DispatchOnValue()

    # Register your overloaded functions:
    @dispatch_on_value.add([1, 2, 3])  # [1, 2, 3] is the pattern to match on
    def _(a):
        assert a == [1, 2, 3]
        # return optional value
        return 3

    @dispatch_on_value.add([4, 5, 6])  # [4, 5, 6] is the pattern to match on
    def _(a):
        assert a == [4, 5, 6]
        # return optional value
        return 4

Then else where in your code, dispatch to the correct function based on the
value of the parameter passed::

    p = [4, 5, 6]
    r = dispatch_on_value.dispatch(p)  # Will call second function above

If no pattern was matched, and hence no function dispatched, the
DispatchFailed class will be raised::

    try:
      p = [7, 8, 9]
      r = dispatch_on_value.dispatch(p)
    except dv.DispatchFailed:
      print 'could not dispatch!'

Features
========

Multiple dispatch on value
--------------------------

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
-----------------------------------------------

The patterns can be as complex and as nested as you like::

    @dispatch_on_value.add({'one': 3, 'animals': ['frog', 'mouse', 34]})

Insert Lambda for wide expression of patterns 
---------------------------------------------

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

Wildcard parameters
-------------------

Use of wildcard tokens ``any_a``, ``any_b``, ... ``any_z`` can ensure values are
identical. e.g.::

    @dispatch_on_value.add([dv.any_a, 'b', 3, [3, 'd', dv.any_a]])
    def _(a):
        # Do something
    
    dispatch_on_value.dispatch(['c', 'b', 3, [3, 'd', 'c']])  # This will match
    dispatch_on_value.dispatch(['f', 'b', 3, [3, 'd', 'f']])  # This will match
    dispatch_on_value.dispatch(['c', 'b', 3, [3, 'd', 'f']])  # This will not match

Match everything in a list with single token
--------------------------------------------

Use the ``all_same`` token to see if all the items in a list match, e.g.::

    @dispatch_on_value.add(['a', dv.all_same(4)])
    def _(a):
        # Do something

    # This will match as the nested list contains all fours
    dispatch_on_value.dispatch(['a', [4,4,4,4,4,4,4]])

You can combine them with the ``any_X`` token::

   @dispatch_on_value.add(['a', dv.all_same(dv.any_a)])
    def _(a):
        # Do something

    # These will match as the nested list contains all the same values
    dispatch_on_value.dispatch(['a', [4,4,4,4,4,4,4]])
    dispatch_on_value.dispatch(['a', [5,5,5]])
    
    # This won't match
    dispatch_on_value.dispatch(['a', [1,2,3]])

These examples are simplistic but a more complex example might be::

    @dispatch_on_value.add(dv.all_same({'age': 32}))
    def _(a):
        # Do something
        
    # This would match since all the items in the list have the same age
    dispatch_on_value.dispatch([{'name': 'john', 'age': 32},
                                {'hair': 'brown', 'age': 32, 'car': 'lada'}])
    
    # This wouldn't match since the ages are different
    dispatch_on_value.dispatch([{'name': 'john', 'age': 32},
                                {'name': 'john', 'age': 9}])

Another example::

    # Match on a list of dictionaries where the name is 'john' and the
    # age is between 30 and 40
    @dispatch_on_value.add(dv.all_same({'name': 'john',
                                        'age': lamba x: 30 < x < 40})
    def _(a):
        # Do something

    # This would match
    dispatch_on_value.dispatch([{'name': 'john', 'age': 32},
                                {'name': 'john', 'age': 37}])
    
    # This would not match
    dispatch_on_value.dispatch([{'name': 'john', 'age': 32},
                                {'name': 'john', 'age': 45}])

No limit on parameters
----------------------

Pass as many extra parameters as you want when dispatching::

    @dispatch_on_value.add([1, 2])
    def _(a, my_abc, my_def):
        assert a == [1, 2]
        # Do something
    
    dispatch_on_value.dispatch([1, 2], 'abc', 'def')

You can also pass keyword parameters::

    @dispatch_on_value.add([3, 4])
    def _(a, my_abc, **kwargs):
        assert 'para1' in kwargs
        # Do something
    
    dispatch_on_value.dispatch([3, 4], 'abc', para1=3)

Methods can also be dispatched
------------------------------

You can dispatch methods on class instances using the add_method decorator::

    dispatch_on_value = dv.DispatchOnValue()

    class MyClass(object):
        @dispatch_on_value.add_method([1, 2, 3])
        def m1(self, a):
            called[0] = 1
            return 2

        @dispatch_on_value.add_method([4, 5, 6])
        def m2(self, a):
            called[0] = 2
            return 3

    my_class = MyClass()

    called = [0]

    p = [4, 5, 6]
    # This will match m2...
    dispatch_on_value.dispatch(p) == 3


Matching on dictionaries is either partial or strict
====================================================

Matching on directories is *partial* by default. This means dictionaries will
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

***********************
Author and Contributors
***********************

Author: `minimind <https://github.com/minimind>`_.

Contributors: `yurtaev <https://github.com/yurtaev>`_, `svisser <https://github.com/svisser>`_.
