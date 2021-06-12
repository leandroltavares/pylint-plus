import pytest
import astroid
import pylint.testutils
from pylint_plus.return_method_checker import MissingReturnChecker


class TestMagicValueChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = MissingReturnChecker

    def test_function_name_suggest_it_should_return(self):
        extracted_node = astroid.extract_node("""
        def get_something():
            pass
        """)

        with self.assertAddsMessages(pylint.testutils.Message(msg_id='magic-constant', node=extracted_node.args[0],
                                                              ),):
            self.checker.visit_functiondef(extracted_node)
            self.checker.leave_functiondef(extracted_node)

    def test_function_name_do_not_suggest_it_should_return(self):
        extracted_node = astroid.extract_node("""
        def do_something():
            pass
        """)

        with self.assertNoMessages():
            self.checker.visit_functiondef(extracted_node)


if __name__ == "__main__":
    pytest.main()
