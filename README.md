# pylint-plus
[![Latest Version](https://img.shields.io/pypi/v/pylint-plus)](https://pypi.python.org/pypi/pylint-plus)
[![License](https://img.shields.io/github/license/leandroltavares/pylint-plus.svg)](LICENSE)

Pylint plugin with good practices extensions

## Running

This is a pylint plugin, so for running it you will need to load the plugin.

```
➜ pylint --load-plugins pylint_plus my_source_code.py 
```

## Checkers
This plugin implements several checkers.

### Magic constant

#### before

This checker detects magic constants in code. 
Magic constants are a code smell and should be replaced by meaningful named constants. 

`example.py`

```python
"""Example file"""
def method_return_magic_constant():
    """Example method"""
    return 42

```
when running lint would yield
```
▶ pylint --load-plugins=pylint_plus example.py
************* Module test
test.py:4:11: R1001: Magic constant found (magic-constant)

------------------------------------------------------------------
Your code has been rated at 5.00/10 (previous run: 5.00/10, +0.00)
```

### after
```python
"""Example file"""
UNIVERSE_ULTIMATE_QUESTION_ANSWER = 42

def method_return_magic_constant():
    """Example method"""
    return UNIVERSE_ULTIMATE_QUESTION_ANSWER

```
running lint again yields
```
▶ pylint --load-plugins=pylint_plus example.py

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```

### Configuration

You may tweak the checker to be more or less strict. For this checker, 
we have the following options available.

| Option                    | Result                                |
|---------------------------|---------------------------------------|
| allow-return-constants    | Allow returning constants             |
| allow-compare-constants   | Allow comparing constants             |
| allow-binary-constants    | Allow binary operation with constants |
| allow-call-args-constants | Allow call args to be constants       |
| allow-subscript-constants | Allow subscript args to be constants  |
| allow-int-constants       | Ignore int constants                  |
| allow-str-constants       | Ignore string constants               |
| allow-float-constants     | Ignore float constants                |

`Boolean` types are ignored by this checker.

### Return method

#### TO BE DOCUMENTED

### Function/Method order

#### TO BE DOCUMENTED

You may find other examples at the [`example/`](example) directory

## Changelog

## v0.0.2

* Initial implementation of the `Function/Method order` checker.
* Fix `Return Method` checker unit tests

## v0.0.1

* Initial implementation of the `Magic constant` checker.
* Initial implementation of the `Return method` checker.