from collections import OrderedDict
from astroid import Attribute

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class FunctionOrderChecker(BaseChecker):
    __implements__ = IAstroidChecker
    name = "function-order"
    priority = -1
    msgs = {
        "R1004": ("Function is out of order", "wrong-function-order",
                  "Function %s should be placed %s after %s"),
        "R1005": ("Method is out of order", "wrong-method-order",
                  "Method %s should be place after %s")
    }

    def __init__(self, linter):
        super().__init__(linter)
        self.function_stack = []
        self.functions = {}
        self.call_seq = OrderedDict()

    def visit_functiondef(self, node):
        self.function_stack.append(node.name)
        if len(self.function_stack) <= 1:
            self.call_seq[node.name] = []
            self.functions[node.name] = node

    def visit_call(self, node):
        callee_name = node.func.attrname if isinstance(node.func, Attribute) else node.func.name
        self.call_seq[self.function_stack[-1]].append(callee_name)

    def leave_functiondef(self, _):
        self.function_stack.pop()

    def leave_module(self, _):
        already_called = set()
        call_order = []
        stack = [callee for call in self.call_seq.values() for callee in call]

        while stack:
            current = stack.pop(0)
            if current not in already_called:
                already_called.add(current)
                call_order.append(current)

            callees = self.call_seq[current]
            for callee in callees:
                if callee not in already_called:
                    stack.insert(0, callee)


        call_index = 0
        def_index = 0

        def_order = [func for func in self.call_seq.keys()]
        

        uncalled = []

        # for func in self.call_seq:
        #     if func in already_called:
        #         expected_def = call_order.pop(0)
        #         if func != expected_def:
        #             self.add_out_of_order_message(func, expected_def)

    def add_out_of_order_message(self, first, second):
        node = self.functions[first]
        if node.is_method():
            self.add_message('wrong-method-order', node=node, args=(first, second))
        else:
            self.add_message('wrong-function-order', node=node, args=(first, second))
