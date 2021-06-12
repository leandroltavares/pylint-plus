#pylint: disable=missing-module-docstring,missing-function-docstring
def example_bad_return():
    return 42


def example_good_return():
    meaningful_constant = 42  # Constant assignments are fine
    return meaningful_constant


def example_bad_compare():
    variable = 0
    if variable < 42:  # Comparison with magic value
        return True  # Boolean returns are not considered
    return False


def example_good_compare():
    variable = 0
    meaningful_constant = 42
    if variable < meaningful_constant:  # Comparison with meaningful value
        return True
    return False


def example_bad_binary_operation():
    variable = 0
    result = variable + 42  # Addition of magic values
    return result


def example_good_binary_operation():
    const1 = 0
    const2 = 42
    result = const1 + const2  # Addition of meaningful values
    return result


def foobar(first, second):
    print(first, second)


def example_bad_call():
    foobar(10, 20)  # Function call with magic values


def examples_good_call():
    first = 10
    second = 20
    foobar(first, second)  # Function call with meaningful values, using variables


def examples_good_call2():
    foobar(first=10, second=20)  # Function call with kwargs


def example_good_collections():
    list_var = [10, 20, 30]
    set_var = {10, 20, 30}
    dict_var = {'a': 1, 'b': 2}
    print(list_var, set_var, dict_var)


def example_bad_slice():
    size = 10
    upper = 1
    sliced = range(size)[0:upper]
    print(sliced)


def example_good_slice():
    size = 10
    lower = 0
    upper = 1
    sliced = range(size)[lower:upper]
    print(sliced)
