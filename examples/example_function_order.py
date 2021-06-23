#pylint: disable=missing-module-docstring,missing-module-docstring,missing-function-docstring,missing-class-docstring,no-self-use,too-few-public-methods
def first():  # First should be defined after second, too keep call order
    pass


def second():
    first()


class Example:
    def first(self):  # First should be defined after second, too keep call order
        pass

    def second(self):
        self.first()

    def before(self):  # 'Before' is placed correctly before 'after'
        self.after()

    def after(self):
        pass


class ExampleInner:
    def outer(self):
        def inner():  # Inner functions are an exception, these must be defined before their usage
            pass

        inner()
