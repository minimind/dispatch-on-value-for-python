===========
Multiple Dispatch on Value
===========

This package provides multiple dispatch on complex nested lists and dictionaries
and (to a var lesser extent) types. Matching on dictionaries is by default fairly
loose e.g. the pattern {'name': 'john'} will match on {'name': 'john, 'age': 32}
even though 'age': 32 isn't in the pattern. You can ensure the dictionaries are
exactly the same by using strict_match.

Typical usage often looks like this::

    from pymultidispatchonvalue import match, expression, ANY_A, ANY_B
    
    def fn1(li, a):
      assert a == {'name': 'john', 'age': 32}
    
    dict1 = {'name': 'john', 'age': 32}
    
    # These will match f1 and as the type isn't a list, tail will always be []:
    (matched, tail) = match(dict1, fn1, li, {'name': 'john', 'age': 32})
    (matched, tail) = match(dict1, fn1, li, {'name': 'john'})
    (matched, tail) = match(dict1, fn1, li, {'age': 32})

    # These will not match:
    (matched, tail) = match(dict1, fn1, li, {'name': 'john', 'age': 76})
    (matched, tail) = match(dict1, fn1, li, {'name': 'lucy', 'age': 32})
    (matched, tail) = match(dict1, fn1, li, {'name': 'lucy'})
   
    #######################################################################
    
    list1 = ['fruit', 'vegetables', 56]
    
    # These will match and tail will be the unmatched tail part of list1.

    def fn2(li, a):
        assert a == 'fruit'
 
    (matched, tail) = match(list1, fn2, li, ['fruit'])
    assert matched and tail = ['vegetables', 56]
    
    ############
    
    def fn3(*args):
        assert args[1] == 'fruit' and args[2] == 'vegetables'

    (matched, tail) = match(list1, fn3, li, ['fruit', 'vegetables'])
    assert matched and tail = [56]
   
    ############

    def fn4(li, a, b, c):
        assert a == 'fruit' and b == 'vegetables' and c == 56

    (matched, tail) = match(list1, fn4, li, ['fruit', 'vegetables', 56])
    assert matched and tail = []

    ############

    # These will not:
    (matched, tail) = match(list1, fn2, li, ['vegetables'])
    (matched, tail) = match(list1, fn3, li, ['vegetables', 56])
   
    #######################################################################
    
    # Also nested data structures can be matched:
    
    list2 = ['fruit', {'orange': 'good', 'apple': 'bad'}]
    
    def fn5(li, a):
        assert a = 'fruit'
 
    (matched, tail) = match(list2, fn5, li, ['fruit'])
    assert matched and tail = [{'orange': 'good', 'apple': 'bad'}]
    
    ############
    
    def fn6(li, a, b):
        assert a = 'fruit' and b = {'orange': 'good', 'apple': 'bad'}
 
    (matched, tail) = match(list2, fn6, li, ['fruit', {'apple': 'bad'}])
    assert matched and tail = []
    
    ############
    
    list3 = ['mice', ['frogs', {'leaps': True, 'green': True}]]
    
    def fn7(li, a):
        assert a == 'frogs'
 
    (matched, tail) = match(list3, fn7, li, ['mice'])
    assert matched and tail = ['frogs', {'leaps': True, 'green': True}]
    
    ############
    
    def fn8(li, a, b):
        assert a == 'frogs' and b == ['frogs', {'leaps': True, 'green': True}]
 
    (matched, tail) = match(list3, fn8, li, ['mice', ['frogs'])
    assert matched and tail = []
    
    ############
    
    def fn8(li, a, b):
        assert a == 'frogs' and b == ['frogs', {'leaps': True, 'green': True}]
 
    (matched, tail) = match(list3, fn8, li, ['mice', ['frogs', {'green': True}])
    assert matched and tail = []
    
    ############
    
    # You can also use lambda's for greater pattern matching:
    
    def fn9(li, a):
      assert a == {'name': 'john', 'age': 32}
    
    dict1 = {'name': 'john', 'age': 32}
    
    # These will match f9 and as the type isn't a list, tail will always be []:
    (matched, tail) = match(dict1, fn9, li, {'age': lambda x: x > 30 and x < 35})
    (matched, tail) = match(dict1, fn9, li, {'name': lambda x: x == 'mary' or x == 'john'})
    
    # This will not match:
    (matched, tail) = match(dict1, fn9, li, {'age': lambda x: x > 40})


(Note the double-colon and 4-space indent formatting above.)

Paragraphs are separated by blank lines. *Italics*, **bold**,
and ``monospace`` look like this.


A Section
=========

Lists look like this:

* First

* Second. Can be multiple lines
  but must be indented properly.

A Sub-Section
-------------

Numbered lists look like you'd expect:

1. hi there

2. must be going

Urls are http://like.this and links can be
written `like this <http://www.example.com/foo/bar>`_.

