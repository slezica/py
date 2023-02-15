# py

Python as a pipeline tool for command-line ninjas.

```
cat notes.txt | py 'line.replace("awk", "py")'
```

## Installation

Just place the `bin/py` file somewhere in your `PATH`, and make it executable.

You will need a `python` executable in the environment (`/usr/bin/env python`). Python 2 and 3 are both supported.

## Basic usage

With no input or flags, `py` executes inline python expresions:

```
$ py '1 + 2'
3
```

Modules are imported automatically, including from the current directory.

```
$ py 'math.factorial(6)'
720
```

## Processing input

`py` has three input handling modes, selected automatically when special
variable names are used in the expression. 

The type of each variable is dependent on the Python version:
  * `TextType` is `unicode` in Python 2, `str` in Python 3
  * `BinaryType` is `str` in Python 2, `bytes` in Python 3

Variable | Input mode
-------- | -------------
`line`   | Eval expression for each line of input, assigning each to `line` in `TextType`
`lines`  | Eval expression once, assigning a list of input lines to `lines`
`input`  | Eval expression once, assigning the entire input to `input`
`bline`   | As `line`, but in `BinaryType`
`blines`  | As `lines`, but with each item in `BinaryType`
`binput`  | As `input`, but in `BinaryType`

So you can do:

```bash
# Replace a word in all lines:
$ ... | py 'line.replace("foo", "bar")'  

# Print longest line:
$ ... | py 'max(lines, key=lambda l: len(l))' 

# Hex-encode entire input:
$ ... | py 'binascii.hexlify(binput)'
```

You can only use one of the three magic variable pairs inside your expression, since they determine the processing mode.