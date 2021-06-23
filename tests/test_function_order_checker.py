import pytest
import astroid
import pylint.testutils
from pylint_plus.function_order_checker import FunctionOrderChecker


class TestFunctionChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = FunctionOrderChecker

    # def test_function_order_when_caller_after_callee(self):
    #     first_node, second_node, call_node = astroid.extract_node("""
    #         def a(): #@
    #             pass
    #         def b(): #@
    #             a() #@
    #         """)
    #
    #     with self.assertAddsMessages(pylint.testutils.Message(msg_id='wrong-function-order', node=first_node,
    #                                                           ),):
    #         self.checker.visit_functiondef(first_node)
    #         self.checker.leave_functiondef(first_node)
    #         self.checker.visit_functiondef(second_node)
    #         self.checker.visit_call(call_node)
    #         self.checker.leave_functiondef(second_node)
    #         self.checker.leave_module(None)
    #
    # def test_function_order_when_caller_before_callee(self):
    #     first_node, call_node, second_node = astroid.extract_node("""
    #         def a(): #@
    #             b() #@
    #         def b(): #@
    #             pass
    #         """)
    #
    #     with self.assertNoMessages():
    #         self.checker.visit_functiondef(first_node)
    #         self.checker.visit_call(call_node)
    #         self.checker.leave_functiondef(first_node)
    #         self.checker.visit_functiondef(second_node)
    #         self.checker.leave_functiondef(second_node)
    #         self.checker.leave_module(None)
    #
    # def test_method_order_when_caller_after_callee(self):
    #     first_node, second_node, call_node = astroid.extract_node("""
    #         class Foo:
    #             def a(self): #@
    #                 pass
    #             def b(self): #@
    #                 self.a() #@ """)
    #
    #     with self.assertAddsMessages(pylint.testutils.Message(msg_id='wrong-method-order', node=first_node,
    #                                                           ),):
    #         self.checker.visit_functiondef(first_node)
    #         self.checker.leave_functiondef(first_node)
    #         self.checker.visit_functiondef(second_node)
    #         self.checker.visit_call(call_node)
    #         self.checker.leave_functiondef(second_node)
    #         self.checker.leave_module(None)
    #
    # def test_method_order_when_caller_before_callee(self):
    #     first_node, call_node, second_node = astroid.extract_node("""
    #         class Foo:
    #             def a(self): #@
    #                 self.b() #@
    #             def b(self): #@
    #                 pass""")
    #
    #     with self.assertNoMessages():
    #         self.checker.visit_functiondef(first_node)
    #         self.checker.visit_call(call_node)
    #         self.checker.leave_functiondef(first_node)
    #         self.checker.visit_functiondef(second_node)
    #         self.checker.leave_functiondef(second_node)
    #         self.checker.leave_module(None)
    #
    # def test_method_order_ignored_when_inner_function(self):
    #     first_node, second_node, call_node = astroid.extract_node("""
    #         class Foo:
    #             def outer(self): #@
    #                 def inner(): #@
    #                     return True
    #                 inner() #@
    #         """)
    #
    #     with self.assertNoMessages():
    #         self.checker.visit_functiondef(first_node)
    #         self.checker.visit_functiondef(second_node)
    #         self.checker.leave_functiondef(second_node)
    #         self.checker.visit_call(call_node)
    #         self.checker.leave_functiondef(first_node)
    #         self.checker.leave_module(None)
    #
    # def test_chained_function_order_with_multiple_calls_to_same_function(self):
    #     def_foo_node, bar_call_node, baz_call_node, def_bar_node, call_qux_node, def_qux_node, call_baz_node, \
    #         def_baz_node = astroid.extract_node("""
    #         def foo(): #@
    #             bar() #@
    #             baz() #@
    #
    #         def bar(): #@
    #             qux() #@
    #
    #         def qux(): #@
    #             baz() #@
    #
    #         def baz(): #@
    #             pass
    #         """)
    #
    #     with self.assertNoMessages():
    #         self.checker.visit_functiondef(def_foo_node)
    #         self.checker.visit_call(bar_call_node)
    #         self.checker.visit_call(baz_call_node)
    #         self.checker.leave_functiondef(def_foo_node)
    #
    #         self.checker.visit_functiondef(def_bar_node)
    #         self.checker.visit_call(call_qux_node)
    #         self.checker.leave_functiondef(def_bar_node)
    #
    #         self.checker.visit_functiondef(def_qux_node)
    #         self.checker.visit_call(call_baz_node)
    #         self.checker.leave_functiondef(def_qux_node)
    #
    #         self.checker.visit_functiondef(def_baz_node)
    #         self.checker.leave_functiondef(def_baz_node)
    #
    #         self.checker.leave_module(None)

    def test_chained_function_out_of_order(self):
        def_foo_node, call_bar_node, call_baz_node, def_bar_node, call_qux_node, def_baz_node, call_bar_node2, \
            call_waldo_node, def_qux_node, call_corge_node, def_corge_node, call_grault_node, def_grault_node, \
            def_waldo_node, def_unkol_node = astroid.extract_node("""
            def foo(): #@
                bar() #@
                baz() #@

            def bar(): #@
                qux() #@

            def baz(): #@
                bar() #@ 
                waldo() #@
                
            def qux(): #@
                corge() #@
                
            def corge(): #@
                grault() #@
            
            def grault(): #@
                pass
            
            def waldo(): #@
                pass
                
            def unkol(): #@
                pass
            """)

        # baz is wronly defined before qux
        # bar is called by foo and later by baz, as it was already called it is previously defined, closer to foo
        # waldo can only be defined after the whole bar call stack is defined, therefore it is placed at the very bottom
        # unkol is not on the call stack, it should be place above them all

        with self.assertNoMessages():
            self.checker.visit_functiondef(def_foo_node)
            self.checker.visit_call(call_bar_node)
            self.checker.visit_call(call_baz_node)
            self.checker.leave_functiondef(def_foo_node)

            self.checker.visit_functiondef(def_bar_node)
            self.checker.visit_call(call_qux_node)
            self.checker.leave_functiondef(def_bar_node)

            self.checker.visit_functiondef(def_baz_node)
            self.checker.visit_call(call_bar_node2)
            self.checker.visit_call(call_waldo_node)
            self.checker.leave_functiondef(def_baz_node)

            self.checker.visit_functiondef(def_qux_node)
            self.checker.visit_call(call_corge_node)
            self.checker.leave_functiondef(def_qux_node)

            self.checker.visit_functiondef(def_corge_node)
            self.checker.visit_call(call_grault_node)
            self.checker.leave_functiondef(def_corge_node)

            self.checker.visit_functiondef(def_grault_node)
            self.checker.leave_functiondef(def_grault_node)

            self.checker.visit_functiondef(def_waldo_node)
            self.checker.leave_functiondef(def_waldo_node)

            self.checker.visit_functiondef(def_unkol_node)
            self.checker.leave_functiondef(def_unkol_node)

            self.checker.leave_module(None)


if __name__ == "__main__":
    pytest.main()
