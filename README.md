# Multiple Dispatch on Value

This package provides multiple dispatch on value complex nested lists and dictionaries.
You can use lambda to do expression matching and an 'any' token that is a
wildcard that ensures identical values can be matched.

## Quick instructions

Start your code with this:

```python
from pymultidispatchonvalue import *

dispatchOnValue = DispatchOnValue()
```

Then register your overloaded functions:

```python
@dispatchOnValue.add([1, 2, 3])  # Primitive type value 1 is the matching pattern
def _(a):
    assert a == 1
    # Do something

@dispatchOnValue.add([4, 5, 6])  # Primitive type value 2 is the matching pattern
def _(a):
    assert a == 2
    # Do something
```

Then later, call the correct overloaded functions:

```python
p = [4, 5, 6]
dispatchOnValue.dispatch(p)  # Will call second function above
```

The return value is True or False, depending upon whether it could match and
call a function or not.

## Some quick examples

1. Match on primitive types (e.g. simple integers):

    ```python
    @dispatchOnValue.add(1)  # Primitive type value 1 is the matching pattern
    def _(a):
        assert a == 1
        # Do something
    
    @dispatchOnValue.add(2)  # Primitive type value 2 is the matching pattern
    def _(a):
        assert a == 2
        # Do something
        
    dispatchOnValue.dispatch(1)  # This will match and call the first function
    dispatchOnValue.dispatch(2)  # This will match and call the second function
    ```

2. Match on lists:

    ```python
    @dispatchOnValue.add(['z', 'b', 3, 'z'])
    def _(a):
        assert a == ['z', 'b', 3, 'z']
        # Do something
    
    dispatchOnValue.dispatch(['z', 'b', 3, 'z'])  # This will match
    dispatchOnValue.dispatch(['a', 'b', 4, 'a'])  # This will not match
    ```

3. Data structure patterns can be arbitrary nested:

    ```python
    @dispatchOnValue.add({'one': 3, 'animals': ['frog', 'mouse']})
    ```

4. Use of wildcard tokens any_a, any_b, ... any_z that will ensure
values are identical. e.g.

    ```python
    @dispatchOnValue.add(['z', 'b', 3, [3, 'd', 'z']])
    def _(a):
        assert a == ['z', 'b', 3, [3, 'd', 'z']]
        # Do something
        
    dispatchOnValue.dispatch([any_a, 'b',   3, [3, 'd', any_a]])  # This will match
    dispatchOnValue.dispatch([any_a, any_a, 3, [3, 'd', any_a]])  # This will not match
    ```

5. Multiple dispatch on value:

    ```python
    @dispatchOnValue.add([1, 2, {'animal': 'goat'}])
    def fn_1(a):
        # Do something
    
    @dispatchOnValue.add([1, 2, {'animal': 'frog'}])
    def fn_2(a):
        # Do something
    
    p = [1, 2, {'animal': 'goat'}]
    dispatchOnValue.dispatch(p)  # This will call fn_1
    
    p = [1, 2, {'animal': 'frog'}]
    dispatchOnValue.dispatch(p)  # This will call fn_2
    
    p = [1, 2, {'animal': 'mouse'}]
    dispatchOnValue.dispatch(p)  # This will not call anything
    ```

6. You can pass as many parameters as you want:

    ```python
    @dispatchOnValue.add([1, 2])  # This is the matching pattern
    def _(a, something, something_else):
        assert a == [1, 2]
        # Do something
    
    dispatchOnValue.dispatch([1, 2], 'abc', 'def')
    ```

## Matching on dictionaries is loose or strict

Matching on directories is loose e.g. the pattern {'name': 'john'} will match on 
{'name': 'john, 'age': 32} even though 'age': 32 isn't in the pattern. You can
ensure the dictionaries are exactly the same by using strict_match.

```python
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
```
