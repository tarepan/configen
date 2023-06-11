"""Test utilities."""

from dataclasses import dataclass

from .utils import default


def test_default_instance():
    """Test `default` with an instance default arugment."""

    @dataclass
    class Child:
        """Could be reused by multiple instances"""
        attr: int = 0

    @dataclass
    class Buggy:
        """Buggy child usage"""
        child: Child = Child(
            attr = 1,)

    buggy_attr_1 = Buggy()
    buggy_attr_2 = Buggy()
    buggy_attr_2.child.attr = 2

    # buggy.child.attr should be 1, but is 2
    assert buggy_attr_1.child.attr == 2, f"Buggy assignment should results in `attr==2`, but is {buggy_attr_1.child.attr}"
    assert buggy_attr_2.child.attr == 2, f"Assign attribute `attr` should be 2, but {buggy_attr_2.child.attr}"

    @dataclass
    class Good:
        """Correct child usage"""
        child: Child = default(Child(attr = 1,))

    good_attr_1 = Good()
    good_attr_2 = Good()
    good_attr_2.child.attr = 2

    assert good_attr_1.child.attr == 1, f"Assign attribute `attr` should be 1, but {good_attr_1.child.attr}"
    assert good_attr_2.child.attr == 2, f"Assign attribute `attr` should be 2, but {good_attr_2.child.attr}"


def test_default_list():
    """Test `default` with an list default arugment."""

    @dataclass
    class Child:
        """List element"""
        attr: int = 0

    # Buggy-like default argument (`child: list[Child] = [Child(attr = 1,)]`) cause 'not allowed' error
    @dataclass
    class Good:
        """Correct child usage"""
        child: list[Child] = default([Child(), Child(attr = 1,)])

    good_attr_1 = Good()
    good_attr_2 = Good()
    good_attr_2.child[1].attr = 2

    assert good_attr_1.child[0].attr == 0, f"Default attribute `attr` should be 0, but {good_attr_1.child[0].attr}"
    assert good_attr_1.child[1].attr == 1, f"Assign  attribute `attr` should be 1, but {good_attr_1.child[1].attr}"
    assert good_attr_2.child[0].attr == 0, f"Default attribute `attr` should be 0, but {good_attr_2.child[0].attr}"
    assert good_attr_2.child[1].attr == 2, f"Assign  attribute `attr` should be 2, but {good_attr_2.child[1].attr}"
