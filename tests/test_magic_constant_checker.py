import pytest
import astroid
import pylint.testutils
from pylint_plus.magic_constant_checker import MagicConstantChecker


class TestMagicValueChecker(pylint.testutils.CheckerTestCase):
    CHECKER_CLASS = MagicConstantChecker

    def test_finds_return_constant(self):
        extracted_node = astroid.extract_node("""
        def test():
            return 42 #@
        """)

        with self.assertAddsMessages(pylint.testutils.Message(msg_id='magic-constant', node=extracted_node.value,),):
            self.checker.visit_return(extracted_node)

    def test_finds_compare_constant_first_operand(self):
        extracted_node = astroid.extract_node('42 < x')

        with self.assertAddsMessages(pylint.testutils.Message(msg_id='magic-constant', node=extracted_node.left,
                                                              ),):
            self.checker.visit_compare(extracted_node)

    def test_finds_compare_constant_second_operand(self):
        extracted_node = astroid.extract_node('x < 42')

        with self.assertAddsMessages(pylint.testutils.Message(msg_id='magic-constant', node=extracted_node.ops[0][1],
                                                              ),):
            self.checker.visit_compare(extracted_node)

    def test_finds_binary_operation_constant_first_operand(self):
        extracted_node = astroid.extract_node('42 + x')

        with self.assertAddsMessages(pylint.testutils.Message(msg_id='magic-constant', node=extracted_node.left,
                                                              ),):
            self.checker.visit_binop(extracted_node)

    def test_finds_binary_operation_constant_second_operand(self):
        extracted_node = astroid.extract_node('x + 42')

        with self.assertAddsMessages(pylint.testutils.Message(msg_id='magic-constant', node=extracted_node.right,
                                                              ),):
            self.checker.visit_binop(extracted_node)

    def test_finds_function_call_constant(self):
        extracted_node = astroid.extract_node('foobar(10, named=30)')

        with self.assertAddsMessages(pylint.testutils.Message(msg_id='magic-constant', node=extracted_node.args[0],
                                                              ),):
            self.checker.visit_call(extracted_node)

    def test_finds_constant_subscript_lower(self):
        extracted_node = astroid.extract_node('col[0:x]')

        with self.assertAddsMessages(pylint.testutils.Message(msg_id='magic-constant',
                                                              node=extracted_node.slice.lower,
                                                              ),):
            self.checker.visit_subscript(extracted_node)

    def test_finds_constant_subscript_upper(self):
        extracted_node = astroid.extract_node('col[x:0]')

        with self.assertAddsMessages(pylint.testutils.Message(msg_id='magic-constant',
                                                              node=extracted_node.slice.upper,
                                                              ),):
            self.checker.visit_subscript(extracted_node)

    def test_not_finds_constant_assignment(self):
        extracted_node = astroid.extract_node('x = 42')

        with self.assertNoMessages():
            pass

    def test_not_finds_return_bool(self):
        extracted_node = astroid.extract_node("""
        def test():
            return False #@
        """)

        with self.assertNoMessages():
            self.checker.visit_return(extracted_node)


if __name__ == "__main__":
    pytest.main()
