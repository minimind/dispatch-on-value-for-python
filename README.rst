============================
Dispatch on Value for Python
============================

This package provides dispatch on value complex for arbitrarily nested lists and
dictionaries. You can use lambda to do expression matching and an 'any'
token that is a wildcard that ensures identical values can be matched. It
is useful for getting rid of complicated and difficult to read
if...elif...elif... chains.

The home page is on github at:

https://github.com/minimind/dispatch-on-value-for-python

Install using pip::

    pip install dispatchonvalue

Unit tests can be run from the source directory using::

    python -m unittest discover -s test

Any queries and comments are welcome and can be sent to me at:

ian.macinnes@gmail.com

***********
Quick guide
***********

Start your code with this::

    import dispatchonvalue as dv

    dispatch_on_value = dv.DispatchOnValue()

Then register your overloaded functions::

    @dispatch_on_value.add([1, 2, 3])
    def _(a):
        assert a == [1, 2, 3]
        # Do something

    @dispatch_on_value.add([4, 5, 6])
    def _(a):
        assert a == [4, 5, 6]
        # Do something

Then later, call the correct overloaded functions::

    p = [4, 5, 6]
    dispatch_on_value.dispatch(p)  # Should call second function above

The return value is True or False, depending upon whether a function
could be matched and called.

*******************
Some quick examples
*******************

1. Multiple dispatch on value::

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

2.  Data structure patterns can be arbitrary nested::

        @dispatch_on_value.add({'one': 3, 'animals': ['frog', 'mouse']})

3. Use of wildcard tokens any_a, any_b, ... any_z that will ensure
   values are identical. e.g.::

        @dispatch_on_value.add([dv.any_a, 'b', 3, [3, 'd', dv.any_a]])
        def _(a):
            # Do something
        
        dispatch_on_value.dispatch(['c', 'b', 3, [3, 'd', 'c']])  # This will match
        dispatch_on_value.dispatch(['f', 'b', 3, [3, 'd', 'f']])  # This will match
        dispatch_on_value.dispatch(['c', 'b', 3, [3, 'd', 'f']])  # This will not match

4. You can pass as many extra parameters as you want when dispatching::

    @dispatch_on_value.add([1, 2])
    def _(a, my_abc, my_def):
        assert a == [1, 2]
        # Do something
    
    dispatch_on_value.dispatch([1, 2], 'abc', 'def')

5. Use lambda's as part of the pattern matching::

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

****************************************************
Matching on dictionaries is either partial or strict
****************************************************

Matching on directories is partial by default. This means dictionaries will
match if all the key/value pairs in the pattern are matched - any extra pairs
will be ignored. You can ensure the dictionaries are exactly the same by using
dispatch_strict() rather than dispatch(). For example::

    @dispatch_on_value.add({'name': 'john', 'age': 32})
    def _(a):
        # Do something

    # These will match because they contain the minimal dictionary items
    dispatch_on_value.dispatch({'name': 'john', 'age': 32})
    dispatch_on_value.dispatch({'name': 'john', 'age': 32, 'sex': 'male'})

    # This will match because it's strict and the pattern is exactly the same
    dispatch_on_value.dispatch_strict({'name': 'john', 'age': 32})

    # This will not match because the dictionary doesn't match exactly
    dispatch_on_value.dispatch_strict({'name': 'john', 'age': 32, 'sex': 'male'})

***********
MIT License
***********

The MIT License (MIT)

Copyright (c) 2014 Ian Macinnes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
