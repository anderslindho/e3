from e3.specification.compare import get_module_difference
from e3.specification.utils import print_modules_as_yaml

EMPTY_MODULE_LIST = {"": [""]}
NON_EMPTY_MODULE_LIST = {
    "foo": ["bar"],
    "baz": ["qux"],
}
NON_EMPTY_MODULE_LIST_AS_YAML = """\
foo:
- bar
baz:
- qux
"""


def test_print_modules_as_yaml(capsys):
    print_modules_as_yaml(NON_EMPTY_MODULE_LIST)
    stdout, stderr = capsys.readouterr()
    assert stdout == NON_EMPTY_MODULE_LIST_AS_YAML
    assert not stderr


def test_get_module_difference_gets_difference():
    difference = get_module_difference(EMPTY_MODULE_LIST, NON_EMPTY_MODULE_LIST)
    assert difference == NON_EMPTY_MODULE_LIST
    assert difference != EMPTY_MODULE_LIST


def test_get_module_difference_does_not_get_difference():
    difference = get_module_difference(NON_EMPTY_MODULE_LIST, EMPTY_MODULE_LIST)
    assert difference == EMPTY_MODULE_LIST
