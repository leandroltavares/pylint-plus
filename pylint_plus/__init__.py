"""pylint-quotes module"""

from __future__ import absolute_import

from pylint_plus.magic_constant_checker import MagicConstantChecker  # noqa: F401
from pylint_plus.return_method_checker import MissingReturnChecker


def plugin_register(linter):
    """This required method auto registers the checker.
    :param linter: The linter to register the checker to.
    :type linter: pylint.lint.PyLinter
    """
    linter.register_checker(MagicConstantChecker(linter))
    linter.register_checker(MissingReturnChecker(linter))


register = plugin_register
