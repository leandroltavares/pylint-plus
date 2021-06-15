from astroid import Attribute

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class FunctionOrderChecker(BaseChecker):
    __implements__ = IAstroidChecker
    name = "function-order"
    priority = -1
    msgs = {
        "R1004": ("Function is out of order", "wrong-function-order",
                  "Function should be defined after its caller"),
        "R1005": ("Method is out of order", "wrong-method-order",
                  "Method should be defined after its caller")
    }

    def __init__(self, linter):
        super().__init__(linter)
        self.function_definitions = {}
        self.function_stack = []

    def visit_functiondef(self, node):
        self.function_stack.append(node.name)
        if len(self.function_stack) <= 1:
            self.function_definitions[node.name] = {'called': False, 'method': node.is_method(), 'node': node}

    def visit_call(self, node):
        callee_name = node.func.attrname if isinstance(node.func, Attribute) else node.func.name
        callee = self.function_definitions.get(callee_name, None)
        if callee and not callee['called']:
            callee['called'] = True
            if callee['method']:
                self.add_message('wrong-method-order', node=callee['node'])
            else:
                self.add_message('wrong-function-order', node=callee['node'])

    def leave_functiondef(self, _):
        self.function_stack.pop()
