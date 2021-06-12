#pylint: disable=missing-module-docstring,missing-function-docstring,too-few-public-methods

def get_something():  # Function is good as it returns something
    return True


def get_something_bad():  # Function has no return, but name indicates it should
    pass


def foo_bar():  # Name does not indicate it should have a return
    pass


def get_something_nested():  # Checker also evaluates inner functions

    def get_inner_something():
        return True

    return get_inner_something()


def __get_something_private():  # Checker also handles "private" function names
    pass


class FooBar:
    def get_something(self):  # Checker differentiates between functions and methods
        pass
