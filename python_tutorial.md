# Python tutorial

Bored of repeating the same tasks again and again? Let the computer do the work, make your life easier and free up time for more interesting tasks.

Python is widely applicable to a variety of tasks, from web-development to data
science to filesystem operations.

We will use Python to automate tasks needed to be performed frequently in computational chemistry.

> This tutorial is valid for Python 3.6 or later.

# Table of Contents

   * [How to use Python?](#how-to-use-python)
   * [Python specifics](#python-specifics)
   * [Fundamental data types](#fundamental-data-types)
      * [Variables](#variables)
      * [Strings](#strings)
      * [Numerical values](#numerical-values)
      * [Boolean values](#boolean-values)
      * [Type conversion](#type-conversion)
   * [Data structures](#data-structures)
      * [Lists](#lists)
      * [Tuples](#tuples)
      * [Dictionaries](#dictionaries)
      * [Conditional statements](#conditional-statements)
   * [Loops](#loops)
      * [For loops](#for-loops)
      * [While loops](#while-loops)
   * [File operations](#file-operations)
   * [Functions](#functions)
      * [Function arguments](#function-arguments)
      * [Example use case](#example-use-case)
   * [Python modules- using external code](#python-modules--using-external-code)
   * [Handling errors](#handling-errors)
   * [Have a go yourself](#have-a-go-yourself)
   * [More advanced topics](#more-advanced-topics)
   <!-- * [Generators](#generators) -->
   * [Classes](#classes)
      * [Thought process](#thought-process)
      * [Writing your own classes](#writing-your-own-classes)
      * [\_\_init\_\_](#__init__)
      * [Inheritance](#inheritance)
      * [Data model](#data-model)
      * [Examples](#examples)

# How to use Python?

Many machines will have Python 2 and Python 3 installed. To check this, type
`python` into a command prompt.

On MacOS:

```bash
$ python
Python 2.7.16 (default, Apr 12 2019, 15:32:40)
[GCC 4.2.1 Compatible Apple LLVM 10.0.1 (clang-1001.0.46.3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

As you can see, Python 2 is loaded. To access Python 3, `python3` must be written.

```bash
$ python3
Python 3.7.3 (default, Mar 27 2019, 09:23:15)
[Clang 10.0.1 (clang-1001.0.46.3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

If Python 3 is not installed, it can be downloaded from the Python online site or
by using Homebrew, `brew install python3`.

When typing `python` or `python3`, a prompt appears waiting for user input. This
is the Python command line interpreter, allowing you to write Python code
directly from the terminal. To re-use code, Python scripts can be saved to a
file, usually with the `py` extension and run like so: `python3 file.py`

# Python specifics

Python relies on indentation to group lines of code together. Most languages
use curly brackets, but by using white space, Python code is generally easier
to read and write. Just try not to mix tabs with spaces as Python will not run
if both are used. 

An important concept in Python is that everything is an object, with a type. To
find out what kind of object you are dealing with, use the function `type()`.

Comments can be written in Python using the `#` symbol, and multi-line comments
are wrapped in triple quotes.

```python

# single line comments

"""
This is a 
multi line
comment
"""
```

# Fundamental data types

## Variables

To be able to pass information around in Python, that data needs to be stored in
a variable, using the `=` sign:

```python
>>> var = 'Here is a sentence.'
>>> var
'Here is a sentence.'
```

## Strings

Text is entered as a `string` using quotation marks:

```python
>>> text = 'This is a string'
>>> type(text)
<class 'str'>
```

Strings can be joined together, or concatenated with the `+` operator:
```python
>>> more_text = 'of more text'
>>> text + more_text
'This is a stringof more text'
```
Notice that no spaces are added when strings are concatenated. To fix this, simply add a space that is placed in between quotation marks:

```python
>>> text + ' ' +  more_text
'This is a string of more text'
```
Or print the text in a formatted string, known as an f-string, with variables
printed using curly braces:

```python
>>> print(f'{text} {more_text}')
This is a string of more text
```

It is useful to look for certain phrases in a string. In Python, there are many
methods that have been implemented to make this easy.

|    Location       |         Command               |
| :---------------: | :---------------------------: |
| Start of string   | `string.startswith(phrase)`   |
| End of string     | `string.endswith(phrase)`     |
| Anywhere          | `if 'phrase' in string`       |


## Numerical values

Whole numbers are known as integers, with decimals called floats, as
they contain floating point values. As you would expect, basic mathematical operations are supported 'out of the box', and integers and floats can be combined in the same expression:

```python
>>> integer1 = 1
>>> integer2 = 4
>>> float1 = 0.2
>>> float2 = 2.0
>>> integer1 + integer2
5
>>> float1 + float2
2.2
>>> integer2 * float2
8.0
>>> integer2 / float2
2.0
>>> integer2 - integer1
3
```

## Boolean values

Boolean values can take the value of `True` or `False`. For example, when
looking for a certain phrase, a boolean variable named `found` can be defined,
set to `False`. When the phrase is found, it can be set to `True`:

```python
found = False

if 'phrase' in line:
    found = True
```

## Type conversion

Often you will need to convert a string into an integer, or maybe a integer into
a float. To convert to a string, use `str()`. To convert to integers and floats,
use `int()` and `float()`.

```python
>>> integer = 3
>>> type(integer)
<class 'int'>
>>> integer = str(integer) # now 'integer' is a string
>>> type(integer)
<class 'str'>

# same for floats
>>> string = '5.0'
>>> string = float(string)
>>> type(string)
<class 'float'>
```

Strings can also be converted into lists. Read on for more information about lists.

```python
>>> string = 'string'
>>> list(string)
['s', 't', 'r', 'i', 'n', 'g']
```

# Data structures

## Lists
Variables are useful, but let's say you wanted to store multiple items together. Lists can be used to achieve this, written using square brackets:

```python
>>> lst = [1, 2, 3, 4, 5]
>>> type(lst)
<class 'list'>
```
Properties of lists can be found using functions that were written to be applied to them. For example, to find how many items are stored in a list, use the function `len()`:

```python
>>> len(lst)
3
```

To access items, or elements, of each list, square bracket notation is used.
Note that 'zero-indexing' is used in Python, with the first element in the list
located at the 0th position:

```python
>>> lst[0]
1
>>> lst[2]
3
```

Lists can be sliced to select a subset of the array. The syntax is as follows: `lst[start : end]`, selecting items from `start` up to but not including the `end`:

```python
>>> lst[:3] # first three items
[1, 2, 3]
>>> lst[2:4]
[3, 4] 
```

Negative indexing is a great way to get items from the end of a list. `lst[-1]`
returns the last element of the list:

```python
>>> lst[-1]
[5]
```

To reverse a list, slice the list from the end backwards, with a third
parameter to the list slice, the increment:

```python
>>> lst[-1::-1]
[5, 4, 3, 2, 1]
```

Lists can be added together with the `+` sign:

```python
>>> [1, 2, 3] + [7, 8, 9]
[1, 2, 3, 7, 8, 9]
```

To add things to the end of a list, use the `append` method, modifying the original list in place:

```python
>>> first = [1, 2, 3]
>>> second = 4
>>> first.append(second)
>>> first
[1, 2, 3, 4]
```

Watch out for unexpected behaviour. If you want to take the list `items = [1, 2, 3]` and multiply every item by 3, you might tempted to do this:

```python
>>> items = [1, 2, 3] 
>>> items * 3
[1, 2, 3, 1, 2, 3, 1, 2, 3]
```

However this just takes the contents of the list and repeats it three times...

To do this, we have to move through the list and multiply each item as we go.

Use a loop! See the loops section [here](#loops)

Sometimes it useful to get the index of each item of a list. This can be done using the
length of the list, or the `enumerate` method:

```python
>>> lst = ['One', 'Two', 'Three']
>>> for index in range(len(lst)):
...     print(index, lst[index])
...
0 One
1 Two
2 Three
```

or

```python
>>> for index, item in enumerate(lst):
...     print(f"Index {index} = {item}")
...
Index 0 = One
Index 1 = Two
Index 2 = Three
```

The enumerate function actually returns a generator object (see later), with each index and item contained in a tuple:

```python
>>> enumerate(lst)
<enumerate object at 0x106feaaf8>
>>> list(enumerate(lst))
[(0, 'One'), (1, 'Two'), (2, 'Three')]
```

For this reason using enumerate is faster than looping through a list of each
element with the `range(len())` syntax.

## Tuples

Lists are mutable data types, where items in the list can be modified after being added to the list. Tuples are similar, but immutable- once a tuple is created, it cannot be changed. This can be useful when dealing with large amounts of data, and python runs faster when using tuples over lists. Tuples are assigned with parentheses:

```python
>>> tup = (1, 2, 3)
```

Tuples are also iterable:

```python
>>> for num in tup:
...     print(num)
...
1
2
3
```

## Sets

Sets are similar to lists, but contain only unique elements.

For example:

```python
>>> lst = [1, 2, 3, 3, 2, 1]
>>> set(lst) # convert list to set
set([1, 2, 3])
```

Sets can be especially useful when comparing data. Python includes built-in
operations to compare elements of different sets and look at the overlap of
different sets.

```python
>>> s1 = set([1,2,3,4,5])
>>> s2 = set([3,4,5,6,7])
>>> s1.union(s2) # join together all elements
set([1, 2, 3, 4, 5, 6, 7])
>>> s1.intersection(s2) # find elements common to both sets
set([3, 4, 5])
>>> s1.difference(s2) # elements in s1 but not in s2
set([1, 2])
>>> s1.symmetric_difference(s2) # elements in either s1 or s2 but not both
set([1, 2, 6, 7])
```

As in mathematics, we can use bitwise operators (|, ^, ~, &) as alternatives for these
methods. These have been overloaded in the class definition of a set- see the
[classes](#classes) section for more information. 

```python
>>> s1 | s2 # elements in s1 or s2- union
set([1, 2, 3, 4, 5, 6, 7])
>>> s1 & s2 # elements in s1 and s2- intersection
set([3, 4, 5])
>>> s1 - s2 # remove all elements in s1 that appear in s2- difference
set([1, 2])
>>> s1 ^ s2 # elements in s1 or s2 but not both- sym. difference
set([1, 2, 6, 7])
>>>
```

## Dictionaries

You may want to store data and refer to it later using another variable. For example, the names and ages of people. This can be done using a list of lists:

```python
>>> people = [['John', 35], ['Gemma', 50], ['David', 25]]
```

To get the names of each person:

```python
>>> for person in people:
...     print(person[0])
...
John
Gemma
David
```

This works but there is no indication of the kind of value that `person[0]` refers to.

A better way is to use a dictionary using key-value pairs, where the key can be used to refer to values at a later time. Create a dictionary using curly braces and separate keys from their values with a colon:

```python
>>> people = {'John': 35, 'Gemma': 50, 'David': 25}
>>> for name in people:
...     print(name) # looping over a dictionary returns the keys
...
John
Gemma
David
```

Much clearer! Ages can be accessed with the `values` method:

```python
>>> for age in people.values():
...     print(age)
...
35
50
25
```

To find the age of John:

```python
>>> people['John']
35
```

But wouldn't it be good to access both names and ages? This can be done with the `items` method:

```python
>>> for name, age in people.items():
...     print(name, age)
...
John 35
Gemma 50
David 25
```

Lists and dictionaries can also be combined. Using a list of dictionaries, the names of each person will be stored as values with the key `name`, same with their ages:

```python
>>> people = [{'name': 'John' , 'age': 35}, 
              {'name': 'Gemma', 'age': 50},
              {'name': 'David', 'age': 25}]

>>> for person in people:
...     print(f"{person['name']} is {person['age']} years old")
...
John is 35 years old
Gemma is 50 years old
David is 25 years old
```

# Conditional statements

Conditional statements let us dictate what we would like to happen in a situation where two results can occur. If you want to see if one number is less than another:

```python
>>> num1 = 10
>>> num2 = 5
>>> if num2 < num1:
...     print('True')
...
True
```

Multiple conditions can be placed together in the same block:

```python
>>> if num1 < num2:
...     print('num1 is less than num2')
... elif num1 == num2: # else if
...     print('num1 is equal to num2')
... else:
...     print('num1 is greater than num2')
...
num1 is greater than num2
```

To negate a comparison, use the `not` keyword:

```python
>>> name = 'Tom'
>>> if name is not 'Jerry':
...    print('Not Jerry')
...
Not Jerry
```

# Loops

## For loops

Every data structure in Python that contains multiple items can be 'iterated'
over using a `for` loop, with the following syntax:

```python
for item in iterable:
  do_something_with_the_item()
```

Now, to multiple every item of the `items` list by 3:

```python
>>> items = [1, 2, 3]
>>> for item in items:
...     multiple = item * 3
...     print(multiple)
...
3
6
9
```

But the original list still contains the original values! The multiples need to be added to a new list:

```python
>>> items
[1, 2, 3] # The loop didn't change the original values

>>> multiples = []
>>> for item in items:
...     multiple = item * 3
...     multiples.append(multiple)
...
>>> multiples
[3, 6, 9]
```

List comprehensions are a nice way to achieve the same thing with less typing:

```python
>>> multiples = [x * 3 for x in items]
>>> multiples
[3, 6, 9]
>>>
```

Useful keywords include `break` and `continue`. The `break` command forces
Python to exit the loop immediately, and the `continue` keyword tells Python to
skip this iteration and move to the next item in the list.


## While loops

The `while` loop can be used together with conditional statements like so:

```python
>>> while num2 < num1:
...     print('num2 = ', num2)
...     num2 += 1 # add one to num2
...
num2 =  5
num2 =  6
num2 =  7
num2 =  8
num2 =  9
```

When `num2` was set to 10, Python broke out of the loop.


# File operations

Lots of menial tasks involve reading text files, modifying them, then writing the data to a new file.
These tasks are simple using Python. To open a file, just use the `open` function. This takes two arguments, the file name and how you'd like to open it: in read mode, `'r'`, write mode, `'w'`, or append mode, `'a'`. There are other options available for binary, such as `'rb'` and `'wb'`.
Remember to close the file after you have finished processing it!

```python
f = open('file1.txt', 'r')
# process file...
f.close()
```

To avoid having to write `f.close()`, use the `with` keyword that automatically closes the file when Python is finished executing code using the file:

```python
with open('file1.txt', 'r') as f:
    # process file...
```

To read the contents of a file, the `file.read()` command can be used. 

With the file called `file1.txt`:
```text
# file1.txt
one
two
three
```

```python
>>> with open('file1.txt', 'r') as f:
...     contents = f.read() # store file in the variable 'contents'
...
>>> contents
'one\ntwo\nthree\n'
```

`f.read()` returns one string containing the contents of the entire file. For
small files, this is not a problem, but for larger files, it is more efficient
to store the data in a list, using `f.readlines()`.

```python
>>> with open('file1.txt', 'r') as f:
...     contents = f.readlines() 
...
>>> contents
['one\n', 'two\n', 'three\n']
```

Again, for larger files storing the entire contents in a list is inefficient. If
you wish to process the file line-by-line, it is possible to do so without
storing the data in a container. Just iterate over the file itself:

```python
>>> with open('file1.txt', 'r') as f:
...     for line in f:
...         print(line)
...
one

two

three

```
Notice that the newline characters at the end of each line are printed, and can be dropped with the
`strip` method, applicable to any string:

```python
>>> with open('file1.txt', 'r') as f:
...     for line in f:
...         print(line.strip())
...
one
two
three
```

This method of reading files is the fastest way of reading in plain text files-
reading binary files is faster, but requires decoding to process the data.

To write to a file, use the `'w'` argument with a file name:

```python
with open('new_file', 'w') as f:
    f.write(content)
```

To write a list to a file:

```python
with open('new_file', 'w') as f:
    for item in list:
        f.write(item + '\n')
```

Don't forget the newline character otherwise all the items will be placed on the
same line!

For file manipulation, have a look at the `os` module, distributed as part of the
standard library.

# Functions

Writing 'procedural' code, line by line, can quickly get very confusing. A clearer way to layout code involves writing functions, pieces of code that can be re-used multiple times.

## Function arguments

In mathematics, a function is something that can receive some input, modify that
input, and produce some output. Functions in programming do the same thing, with
the input included as arguments to the function. For example:

```python
def print_name(name):
    print('My name is', name)

print_name('Mary')
print_name('David')

# Output:
# My name is Mary
# My name is David
```
The function `print_name` is taking the name given as an argument and using the
value in the function.

In order for Python functions to use the data that you give them, arguments
need to be defined, otherwise an error is given with variables used in the
function not being defined:

```python
def func():
    print(arg1)

func()

# Traceback (most recent call last):
#   File "<stdin>", line 11, in <module>
#   File "<stdin>", line 9, in func
# NameError: name 'arg1' is not defined
```

Default values can be given, which are automatically used if no value is given:

```python
def add(num1, num2 = 5):
    print(num1 + num2)

add(5) 
add(10, 20) 

# Output:
# 10 # only one argument passed
# 30 # can overwrite the default value
```

Keyword arguments let you keep track of variables more easily- you know exactly
what you are passing into each function. By defining the argument as `arg =
None`, the user must write `arg = some value` when using the function in order
to pass in a value, or an error is thrown:

```python
def add(val1, val2 = None):
    print(val1 + val2)

add(1)

# Output:
# Traceback (most recent call last):
#   File "<stdin>", line 4, in <module>
#   File "<stdin>", line 2, in addition
# TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'
```

To fix the error:

```python
addition(1, val2 = 10)

# Output:
# 11
```
This forces you to write readable code- it is clear that the number 10 is being
assigned to the variable `val2`. Here, val2 is known as a keyword argument,
defining the name of the argument in the function call.

To return objects from a function, simply use the `return` keyword:
```python
def add_10(num):
    return num + 10

result = add_10()
print(result)

# Output:
# 20 
```

The result was passed from the function and stored in the variable `result`.

## Example use case

To add atomic numbers to a list of coordinates in an xyz format,
you could write something like this:

```text
# coords.xyz
5

C  13.456 12.321 13.054
H  11.222 12.542 10.342
H  10.321  9.896  5.341
O   3.451  5.759  4.531
N   8.421  9.582 10.888
```

```python
atnums = {}
atnums['C'] = 6.0
atnums['H'] = 1.0
atnums['N'] = 7.0
atnums['O'] = 8.0

new_coords = []
with open('coords.xyz', 'r') as f:
    for line in f.readlines()[2:]: # list slicing to only select the coordinates
        sym, x, y, z = line.split()
        atnum = atnums[sym] 
        new_coords.append(f"{sym:<2} {atnum:<4} {x:<6} {y:<6} {z:<6}\n") #string formatting

print(str(len(new_coords)) + '\n')
for line in new_coords:
    print(line, end='')

# Output:
# 5
# 
# C  6.0  13.456 12.321 13.054 
# H  1.0  11.222 12.542 10.342
# H  1.0  10.321 9.896  5.341
# O  8.0  3.451  5.759  4.531
# N  7.0  8.421  9.582  10.888
```

This block defines a dictionary of atomic numbers for carbon, hydrogen, nitrogen
and oxygen, reads in the coordinates, finds the corresponding atomic number,
then adds the number into
the line and appends the new line to the `new_coords` list.

The code above can be re-written using functions, defining a function using the `def`
keyword. Comments can be added to each function definition using triple quotes,
called a docstring.

```python
def read_file(file): 
    """
    Reads a file into Python, overlooking the first two lines. Returns a list
    of the file contents
    """
    
    with open(file, 'r') as f:
        contents = f.readlines()[2:]
    return contents

def get_atomic_number(symbol):
    """
    Returns the atomic number of a given chemical element
    """

    atnums = {}
    atnums['C'] = 6.0
    atnums['H'] = 1.0
    atnums['N'] = 7.0
    atnums['O'] = 8.0

    return atnums[symbol]    

def add_atomic_number(line):
    """
    Finds the atomic number of the atom passed as an argument and returns a
    formatted string including that atomic number
    """
    
    sym, x, y, z = line.split()
    atnum = get_atomic_number(sym) 
    return f"{sym:<2} {atnum:<4} {x:<6} {y:<6} {z:<6}\n"

def modify_coords(coords):
    """
    Modifies coordinates and returns a new list
    """

    new_coords = []
    for line in coords:
        line = add_atomic_number(line)
        new_coords.append(line)
    return new_coords

def print_coordinates(coordinates):
    """
    Prints out the coordinates in an xyz format
    """

    print(str(len(coordinates)) + '\n') 
    # the length of list is an integer that needs converting to a string before adding newlines
    for coord in coordinates:
        print(coord, end='')

def main():

    coords = read_file('coords.xyz')
    new_coords = modify_coords(coords)
    print_coordinates(new_coords)

main()

# Output:
# 5
# 
# C  6.0  13.456 12.321 13.054
# H  1.0  11.222 12.542 10.342
# H  1.0  10.321 9.896  5.341 
# O  8.0  3.451  5.759  4.531 
# N  7.0  8.421  9.582  10.888
```

In this example, the code using functions is longer than the procedural
version, but now we can re-use the code! The function `modify_coords` can be
used to modify 1000 xyz files in one go if we wanted to:

```python
lst = [file1, file2, file3...]

for file in lst:
    coords = read_file(lst)
    new_coords = modify_coords(coords)
    write_file(new_coords)
```

It's that easy! As your programs get longer, you will appreciate how useful
functions can be.


# Python modules- using external code

In Python, the `import` keyword gives you access to code that sits outside of
the file that is being written. To include the math module that comes
pre-installed with Python, type `import math`:

```python
>>> import math
>>> math.pi
3.141592653589793
```

Attributes of the math module are accessed through `math.attribute`. As shown
above, the value of $\pi$ can be obtained with `math.pi`. 

To give an alias to an imported package, use `import ... as ...`

```python
import matplotlib.pyplot as plt
```

This saves you from having to type out `matplotlib.pyplot` every time you use code
from that module.

Many useful modules and packages have been written by others, and can be
installed using the `pip` command from a shell prompt:

To install the NumPy package:
```bash
$ pip install numpy
```

This command will download the NumPy package from the Python Package Index,
PyPi, and install it in a location that Python can access by default. This
location can be found by typing

```python
>>> import site
>>> site.getsitepackages()
['/usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages']
```

# Handling errors

Python error messages are generally quite helpful:

```python
>>> number = 30
>>> print("Printing number: " + number)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate str (not "int") to str
```
Here, number is an integer and cannot be combined with a string.
To overcome this, you can convert `number` to a string:

```python
>>> number = 30
>>> print("Printing number: " + str(number))
Printing number: 30
```

or use a formatted string, automatically converting to a string:

```python
>>> print(f"Printing number: {number}")
Printing number: 30
```

If you have some idea of what kinds of errors might occur, you can catch them
using a `try/except` statement. For example:

```python
number = 30
try:
    print("Printing number: " + number)
except TypeError:
    print(f"Printing number: " + str(number))
```

Here we are predicting that `number` may not be a string, and adding in code to 
deal with that event if it occurs.

For more information, see [here](https://www.programiz.com/python-programming/exceptions).

# Have a go yourself

Using the pointers given above, you can definitely start writing some useful
programs! Many useful packages exist on PyPi, I recommend looking there, as many
solutions to problems you might come across will have already been implemented
in Python. See [here](https://pypi.org/).

From here onwards, more advanced topics will be discussed, including generators
and classes.

# More advanced topics

<!-- # Generators -->

# Classes

## Thought process

Writing functions are very useful, enabling the user to calling the same block
of code over and over. However, there is another branch of programming that
allows users to write code in terms of real-world objects, called
object-oriented programming.

In the real-world, objects have physical attributes and behaviour. For example,
humans have fingers, they have age, a height, and a weight. These are all
attributes. Behaviours associated with humans include speaking, eating and
walking. In OOP, variables are known as attributes, and functions relating to
the behaviour of an object are called methods.

Objects can be written as classes, with the syntax `class object`. At the start
of the tutorial, I [mentioned](#python-specifics) that everything in Python is
an object with a defined type. This means that when we create a list, all we are
doing is creating an *instance* of the `list` class.

```python
>>> lst = list() # create an instance of the list class
>>> lst # empty list
[]
```

When we say `item = list(item)` to convert the item into a list, we are really creating
an instance of the `list` class, and assigning that back to the variable called `item`.

## Writing your own classes

The definition of a class can be empty! Using the `pass` keyword that lets
Python know to do nothing. Attributes can assigned with the dot notation.

```python
class Human:
    pass

human = Human()
human.hands = 2
```

## \_\_init\_\_

We know that humans should have two hands- that shouldn't be something that a
user has to add manually. So we can assign a `hands` attribute to every example
of a Human that we create when calling the `Human` class i.e. `human = Human()`
To do this, we use the `__init__` method, a reserved name in Python. Even though
it is not explicitly declared in Python3, every user-defined class in Python is
derived from the `Object` class, and can have an `__init__` method with the
first argument of `self`.

The attributes of each instance are tied to the class by using the `self`
keyword. For example, creating a `Human` class with two hands:

```python
class Human:

    def __init__(self)
        self.hands = 2


human = Human() # create an instance of the Human class
print(human.hands) # each human has two hands

# Output:
# 2
```

We can think of each instance of a class replacing the word `self`.

We can also assign items to each instance of the class when we *instantiate* the
class. As the `__init__` method is essentially a Python function, we just add
items to the function definition, and then assign them to the object by using
the `self` keyword:

```python
class Human:

    def __init__(self, name, age, height):
        self.hands = 2
        self.name = name
        self.age = age
        self.height = height # in cm
    
```

The values can then be passed in when creating the object instance:

```python
mike = Human('Mike', 19, 170)
print("Mike's age =", mike.age)
print("Mike's height =", mike.height, "cm")

# Output:
# Mike's age = 19
# Mike's height = 170 cm
```

> Aside: the double underscore indicates a reserved value in Python. An instance of the
> `Object` class uses a double underscore, or 'dunder' method, in a certain way.
> See [here](#data-model).

We can also add behaviour so that our `Human` object acts like a real person.
This is done by adding methods to the class definition. We can create a method
that increases a person's age when they have a birthday:

```python
class Human:

    def __init__(self, name, age, height):
        self.hands = 2
        self.name = name
        self.age = age
        self.height = height # in cm

    def had_birthday(self):
        self.age += 1
```

Two important things to note. Firstly, the self keyword is required as an
argument to modify parameters of each instance of the class. Secondly, the age
doesn't need to be returned from the method, as the age attribute is tied to the
class instance. In other words, calling the method automatically modifies the
attributes in the method- there is no need to return the value and save it into
a variable.

```python
kate = Human('Kate', 29, 180)
print("Kate's age =", kate.age)
print('Kate had a birthday')
kate.had_birthday()
print("Kate's age =", kate.age)

# Output:
# Kate's age = 29
# Kate had a birthday
# Kate's age = 30
```

We can see that calling `kate.had_birthday()` increased her age by a year.

## Inheritance

Inheritance is a neat way of writing less code to achieve the same results. In
OOP, attributes and behaviour can be shared between objects. For example,
bananas and apples are both fruits with a colour and shape. So we could make a
`Food` class, with a `Fruit` class that inherits all the properties of a food
item, and extends the class with its own meaning:

```python

class Food:

    def __init__(self, name, colour, food_type):
        self.name = name
        self.colour = colour
        self.type = food_type # note using type as a function argument is bad practice

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_colour(self):
        return self.colour

class Fruit(Food):

    def __init__(self, name, colour):
        super().__init__(name, colour, 'Fruit') # food_type = Fruit

# Usage
>>> banana = Fruit('banana', 'yellow')
>>> banana.get_type()
'Fruit'
```

Here, all of the attributes and methods of the `Food` class are available to the
`Fruit` class, so by calling `banana.get_type()`, we are really calling
`Food.get_type()`  on the `food_type` of the `Fruit` class. The attributes of
the `Fruit` class that we would like to pass to `Food` are done so using the
`super().__init__()` method, supplying arguments to the constructor of the
parent class.

In the example of people, we can have `Adult` and `Child` classes inheriting
from `Human`, and even `Man`, `Woman`, `Boy` and `Girl` classes inheriting from
those sub-classes:

```python
# human.py

class Human:

    def __init__(self, name, age, height, gender):
        self.hands = 2
        self.name = name
        self.age = age
        self.height = height # in cm
        self.gender = gender

    def had_birthday(self):
        self.age += 1
    
    def is_male(self):
        return self.gender.lower == 'male'
    
    def is_female(self):
        return self.gender.lower == 'female'

class Adult(Human):
    
    def __init__(self, name, age, height, gender, children = None):
        super().__init__(name, age, height, gender)
        self.children = children
        self.has_children = False
        if self.children > 0:
            self.has_children = True
    
    def is_parent(self):
        return self.has_children

class Man(Adult):
        
    def __init__(self, name, age, height, children):
        super().__init__(name, age, height, 'Male', children)

class Woman(Adult):

    def __init__(self, name, age, height, children):
        super().__init__(name, age, height, 'Female', children)

class Child(Human):

    def __init__(self, name, age, height, gender):
        super().__init__(name, age, height, gender)
        if self.age >= 18:
            raise ValueError('Too old to be a child!')

class Boy(Child):

    def __init__(self, name, age, height):
        super().__init__(name, age, height, 'Male')

class Girl(Child):

    def __init__(self, name, age, height):
        super().__init__(name, age, height, 'Female')

# Usage

# >>> david = Boy('David', 20, 150)
# Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#  File "human.py", line 54, in __init__
#     super().__init__(name, age, height, 'Male')
#   File "human.py", line 44, in __init__
#     raise ValueError('Too old to be a child!')
# ValueError: Too old to be a child!

# >>> jenny = Woman('Jenny', 30, 170, children = 2)
# >>> jenny.is_parent()
# True
```

## Data model

The Python data model is a term that describes the use of special methods that
the Python interpreter calls when you write a command in using a certain syntax.
For more details, [this video](https://www.youtube.com/watch?v=cKPlPJyQrt4)
describes the data model in a better way than I can. In essence when you write
`len(item)`, these methods let Python know what the length of that object means.

For example, the length of a list is defined as the number of elements. But to
add two strings together represents something different than adding two
integers.

These 'special' methods are written with double underscores before and after
the method names. Examples include `__len__`, `__add__` and `__iter__`. The
`__iter__` methods tells Python how to iterate over an object, say in a for
loop. Therefore the class definitions of lists, tuples, dictionaries, sets, and
strings all contain an `__iter__` method.

Each special method a corresponding syntax that is easier for the end user to
implement- instead of typing `object.__add__(other object)`, just type `object +
other object`.

| Definition                         | syntax            |
| :--------:                         | :----:            |
| `object.__add__(self, other)`      | `object + other`  |
| `object.__sub__(self, other)`      | `object - other`  |
| `object.__mul__(self, other)`      | `object * other`  |
| `object.__matmul__(self, other)`   | `object @ other`  |
| `object.__truediv__(self, other)`  | `object / other`  |
| `object.__floordiv__(self, other)` | `object // other` |
| `object.__mod__(self, other)`      | `object % other`  |
| `object.__pow__(self, other)`      | `object ** other` |
| `object.__lshift__(self, other)`   | `object < other`  |
| `object.__rshift__(self, other)`   | `object > other`  |
| `object.__and__(self, other)`      | `object & other`  |
| `object.__xor__(self, other)`      | `object ^ other`  |
| `object.__or__(self, other)`       | `object \| other`  |

There are many other special methods, read the [Python
documentation](https://docs.python.org/3/reference/datamodel.html) for more
details.

One special method that should be included whenever you define a class is the
`__repr__` method i.e. how the object is displayed when you print it out.

In our `Human` class:

```python
class Human:

    def __init__(self, name, age, height):
        self.hands = 2
        self.name = name
        self.age = age
        self.height = height # in cm

    def __repr__(self):
        return f"{self.name.capitalize()}: {self.age} yo, {self.height} cm"

    def had_birthday(self):
        self.age += 1

# Usage
>>> jim = Human('jim', 35, 190)
>>> jim
Jim: 35 yo, 190 cm
```

## Examples

For chemists, it would make sense to create an `Atom` object. So what would this
object contain? Probably chemical symbols, atomic numbers, coordinates and
covalent radii.

Here is an example of the definition, or the blueprint, of an atom:

```python
class Atom:

    def __init__(self, sym, atnum, x, y, z):
        self.sym = sym
        self.atnum = atnum
        self.x = x
        self.y = y
        self.z = z
```

This would require the user to enter both the chemical symbol and atomic number,
even though they are intrinsically linked. To account for this:

```python
class Atom:

    def __init__(self, x, y, z, sym = None, atnum = None): 
        # keyword arguments must come after positional
        if sym is not None:
            self.sym = sym
            self.atnum = self.get_atnum()
        if atnum is not None:
            self.atnum = atnum
            self.sym = self.get_symbol()
        self.x = x
        self.y = y
        self.z = z

    def get_atnum(self):
        """
        Returns the atomic number of a given atom
        """
        atnums = { 'H'  : 1, 
                   'He' : 2,
                   'Li' : 3, 
                    ...  
                 }
        return atnums[self.sym]

    def get_symbol(self):
        """
        Returns the chemical symbol of a given atom
        """
        symbols = { 1 : 'H', 
                    2 : 'He',
                    3 : 'Li', 
                    ...  
                 }
        return symbols[self.atnum]
```

It may also make sense to include a list or tuple of coordinates, instead of
having to write out each x, y, and z component:

```python
class Atom:

    def __init__(self, sym = None, atnum = None, coords = None): 
        # keyword arguments must come after positional
        if sym is not None:
            self.sym = sym
            self.atnum = self.get_atnum()
        if atnum is not None:
            self.atnum = atnum
            self.sym = self.get_symbol()
        self.coords = coords
        self.x, self.y, self.z = self.coords # list unpacking

    def get_atnum(self):
        """
        Returns the atomic number of a given atom
        """
        atnums = { 'H'  : 1, 
                   'He' : 2,
                   'Li' : 3, 
                    ...  
                 }
        return atnums[self.sym]

    def get_symbol(self):
        """
        Returns the chemical symbol of a given atom
        """
        symbols = { 1 : 'H', 
                    2 : 'He',
                    3 : 'Li', 
                    ...  
                 }
        return symbols[self.atnum]
```

This also allows us to implement the meaning of iterating over an atom. What
would this mean in reality? Probably moving through each x, y and z component of
the atom's position in space:

```python
class Atom:

    def __init__(self, sym = None, atnum = None, coords = None): 
        # keyword arguments must come after positional
        if sym is not None:
            self.sym = sym
            self.atnum = self.get_atnum()
        if atnum is not None:
            self.atnum = atnum
            self.sym = self.get_symbol()
        self.coords = coords
        self.x, self.y, self.z = self.coords # list unpacking

    def __repr__(self): #formatted floats to 5 decimal places
        return f"Atom: {self.sym}, coords = {self.x:6.5f}, {self.y:6.5f}, {self.z:6.5f}"

    def __iter__(self):
        return iter(self.coords)

    def get_atnum(self):
        """
        Returns the atomic number of a given atom
        """
        atnums = { 'H'  : 1, 
                   'He' : 2,
                   'Li' : 3, 
                    ...  
                 }
        return atnums[self.sym]

    def get_symbol(self):
        """
        Returns the chemical symbol of a given atom
        """
        symbols = { 1 : 'H', 
                    2 : 'He',
                    3 : 'Li', 
                    ...  
                 }
        return symbols[self.atnum]
```

Here's how you would use the `Atom` class:

```python
>>> hydrogen = Atom('H', coords = (1,2,3))
>>> hydrogen # print to screen
Atom: H, coords = 1.00000, 2.00000, 3.00000
>>> hydrogen.get_atnum()
1
```

This class could be extended to work with translations in space or inter-atomic
distances. A molecule class could also be created that stores a list of `Atom`
objects.
