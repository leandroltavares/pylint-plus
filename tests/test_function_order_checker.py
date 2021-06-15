import pytest
import astroid
import pylint.testutils
from pylint_plus.function_order_checker import FunctionOrderChecker


class TestFunctionChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = FunctionOrderChecker

    def test_function_order_when_caller_after_callee(self):
        first_node, second_node, call_node = astroid.extract_node("""
            def first(): #@
                pass
            def second(): #@
                first() #@
            """)

        with self.assertAddsMessages(pylint.testutils.Message(msg_id='wrong-function-order', node=first_node,
                                                              ),):
            self.checker.visit_functiondef(first_node)
            self.checker.leave_functiondef(first_node)
            self.checker.visit_functiondef(second_node)
            self.checker.visit_call(call_node)
            self.checker.leave_functiondef(second_node)

    def test_function_order_when_caller_before_callee(self):
        first_node, call_node, second_node = astroid.extract_node("""
            def first(): #@
                second() #@
            def second(): #@
                pass
            """)

        with self.assertNoMessages():
            self.checker.visit_functiondef(first_node)
            self.checker.visit_call(call_node)
            self.checker.leave_functiondef(first_node)
            self.checker.visit_functiondef(second_node)
            self.checker.leave_functiondef(second_node)

    def test_method_order_when_caller_after_callee(self):
        first_node, second_node, call_node = astroid.extract_node("""
            class Foo:
                def first(self): #@
                    pass
                def second(self): #@
                    self.first() #@ """)

        with self.assertAddsMessages(pylint.testutils.Message(msg_id='wrong-method-order', node=first_node,
                                                              ),):
            self.checker.visit_functiondef(first_node)
            self.checker.leave_functiondef(first_node)
            self.checker.visit_functiondef(second_node)
            self.checker.visit_call(call_node)
            self.checker.leave_functiondef(second_node)

    def test_method_order_when_caller_before_callee(self):
        first_node, call_node, second_node = astroid.extract_node("""
            class Foo:
                def first(self): #@
                    self.second() #@
                def second(self): #@
                    pass""")

        with self.assertNoMessages():
            self.checker.visit_functiondef(first_node)
            self.checker.visit_call(call_node)
            self.checker.leave_functiondef(first_node)
            self.checker.visit_functiondef(second_node)
            self.checker.leave_functiondef(second_node)

    def test_method_order_ignored_when_inner_function(self):
        first_node, second_node, call_node = astroid.extract_node("""
            class Foo:
                def outer(self): #@
                    def inner(): #@
                        return True
                    inner() #@
            """)

        with self.assertNoMessages():
            self.checker.visit_functiondef(first_node)
            self.checker.visit_functiondef(second_node)
            self.checker.leave_functiondef(second_node)
            self.checker.visit_call(call_node)
            self.checker.leave_functiondef(first_node)


if __name__ == "__main__":
    pytest.main()
