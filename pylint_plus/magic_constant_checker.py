import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class MagicConstantChecker(BaseChecker):
    __implements__ = IAstroidChecker
    name = "magic-constant"
    priority = -1
    msgs = {
        "R1001": ("Magic constant found", "magic-constant",
                  "Magic constant found, consider replacing it with a meaningful constant")
    }

    options = (('allow-return-constants', {'default': False, 'type': 'yn', 'metavar': '<y_or_n>',
                                           'help': 'Allow returning constants'}),
               ('allow-compare-constants', {'default': False, 'type': 'yn', 'metavar': '<y_or_n>',
                                            'help': 'Allow comparing constants'}),
               ('allow-binary-constants', {'default': False, 'type': 'yn', 'metavar': '<y_or_n>',
                                           'help': 'Allow binary operation with constants'}),
               ('allow-call-args-constants', {'default': False, 'type': 'yn', 'metavar': '<y_or_n>',
                                              'help': 'Allow call args to be constants'}),
               ('allow-subscript-constants', {'default': False, 'type': 'yn', 'metavar': '<y_or_n>',
                                              'help': 'Allow subscript args to be constants'}),
               ('allow-int-constants', {'default': False, 'type': 'yn', 'metavar': '<y_or_n>',
                                        'help': 'Ignore int constants'}),
               ('allow-str-constants', {'default': False, 'type': 'yn', 'metavar': '<y_or_n>',
                                        'help': 'Ignore string constants'}),
               ('allow-float-constants', {'default': False, 'type': 'yn', 'metavar': '<y_or_n>',
                                          'help': 'Ignore float constants'}),)

    def __init__(self, linter):
        super().__init__(linter)
        self.allowed_types = self._evaluate_allowed_types()

    def visit_return(self, node):
        if not self.config.allow_return_constants:
            self._evaluate_constant(node.value)

    def visit_compare(self, node):
        if not self.config.allow_compare_constants:
            self._evaluate_constant(node.left)
            for _, op_value in node.ops:
                self._evaluate_constant(op_value)

    def visit_binop(self, node):
        if not self.config.allow_binary_constants:
            self._evaluate_constant(node.left)
            self._evaluate_constant(node.right)

    def visit_call(self, node):
        if not self.config.allow_call_args_constants:
            for arg in node.args:
                self._evaluate_constant(arg)

    def visit_subscript(self, node):
        if not self.config.allow_subscript_constants:
            self._evaluate_constant(node.slice.lower)
            self._evaluate_constant(node.slice.upper)

    def _evaluate_constant(self, node):
        # Special treatment to booleans, as isinstance(False, int) returns True
        if isinstance(node, astroid.node_classes.Const) and \
                isinstance(node.value, self.allowed_types) and \
                not isinstance(node.value, bool):
            self.add_message('magic-constant', node=node)

    def _evaluate_allowed_types(self):
        types = []
        if not self.config.allow_int_constants:
            types.append(int)
        if not self.config.allow_str_constants:
            types.append(str)
        if not self.config.allow_float_constants:
            types.append(float)
        return tuple(types)
