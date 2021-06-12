from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class MissingReturnChecker(BaseChecker):
    __implements__ = IAstroidChecker
    name = "missing-return"
    priority = -1
    msgs = {
        "R1002": ("Function name indicates it should return", "function-missing-return",
                  "Function should have a return based on name"),
        "R1003": ("Method name indicates it should return", "method-missing-return",
                  "Method should have a return based on name")
    }
    prefixes = ['get', 'return', 'retrieve', 'fetch', 'list', 'map', 'query']

    def __init__(self, linter):
        super().__init__(linter)
        self.function_stack = []

    def visit_functiondef(self, node):
        self.function_stack.append([])

    def visit_return(self, node):
        self.function_stack[-1].append(node)

    def leave_functiondef(self, node):
        if self._evaluate_name_starts_with_returnable_prefix(node.name) \
                and len(self.function_stack[-1]) == 0:
            message_type = 'method-missing-return' if node.is_method() else 'function-missing-return'
            self.add_message(message_type, node=node)
        self.function_stack.pop()

    def _evaluate_name_starts_with_returnable_prefix(self, name):
        return any(self._sanitize_function_name(name).startswith(prefix) for prefix in self.prefixes)

    @staticmethod
    def _sanitize_function_name(name):
        return name.replace('_', '')
