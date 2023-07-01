"""Test merge."""

from __future__ import annotations
from dataclasses import dataclass

from .merge import merge
from .utils import default


#### None-None #########################################################################
def test_merge_none_none():
    """Test `merge` with none-none primitive reassignment."""
    merged = merge(None, None)
    assert merged is None
#### /None-None ########################################################################


#### None-Primitive ####################################################################
def test_merge_none_primitive():
    """Test `merge` with none-primitive reassignment."""
    merged = merge(None, 1)
    assert merged is 1
#### /None-Primitive ###################################################################


#### Tuple-Tuple #######################################################################
def test_merge_tuple_non_nest():
    """Test `merge` with non-nest tuple-tuple element."""
    merged = merge(  (1, 2, 3,),
                     (4, 5, 6,))
    assert merged == (4, 5, 6,)
#### /Tuple-Tuple ######################################################################


#### List-List #########################################################################
def test_merge_list_primitive():
    """Test `merge` with non-nest list-list element."""
    merged = merge(  [1, 2, 3,],
                     [4, 5, 6,])
    assert merged == [4, 5, 6,]


def test_merge_list_template():
    """Test `merge` with non-nest list-list template."""

    merged = merge(  [1,],
                     [4, 5, 6,])
    assert merged == [4, 5, 6,]
#### /List-List ########################################################################


#### Dict-Dict #########################################################################
def test_merge_no_nest_exclusive():
    """Test `merge` with non-nest dict-dict shallow."""
    merged =   merge({"a": 1,       },
                     {        "b": 2})
    assert merged == {"a": 1, "b": 2}


def test_merge_no_nest_full_update():
    """Test `merge` with non-nest dict-dict deep."""
    merged =   merge({"a": 1},
                     {"a": 2})
    assert merged == {"a": 2}


def test_merge_no_nest_partial_update():
    """Test `merge` with non-nest dict-dict shallow & deep."""
    merged =   merge({"a": 1, "b": 3},
                     {"a": 2,       })
    assert merged == {"a": 2, "b": 3}


def test_merge_no_nest_partial_new():
    """Test `merge` with non-nest dict-dict deep & shallow."""
    merged =   merge({"a": 1,       },
                     {"a": 2, "b": 3})
    assert merged == {"a": 2, "b": 3}


def test_merge_nest_exclusive():
    """Test `merge` with nest dict-dict shallow."""
    merged = merge(  {"a": {"aa": 1}                },
                     {                "b": {"bb": 2}})
    assert merged == {"a": {"aa": 1}, "b": {"bb": 2}}


def test_merge_nest_full_update():
    """Test `merge` with nest dict-dict deep->deep."""
    merged = merge(  {"a": {"aa": 1}},
                     {"a": {"aa": 2}})
    assert merged == {"a": {"aa": 2}}


def test_merge_nest_partial_update():
    """Test `merge` with nest dict-dict shallow & deep."""
    merged =   merge({"a": {"aa": 1}, "b": {"bb": 2}},
                     {"a": {"aa": 2},              })
    assert merged == {"a": {"aa": 2}, "b": {"bb": 2}}


def test_merge_nest_partial_new():
    """Test `merge` with nest dict-dict deep & shallow."""
    merged =   merge({"a": {"aa": 1}                },
                     {"a": {"aa": 2}, "b": {"bb": 3}})
    assert merged == {"a": {"aa": 2}, "b": {"bb": 3}}


def test_merge_nest_child_exclusive():
    """Test `merge` with nest dict-dict deep & shallow."""
    merged = merge(  {"a": {"aa": 1,        }},
                     {"a": {         "AA": 2}})
    assert merged == {"a": {"aa": 1, "AA": 2}}


def test_merge_nest_child_partial_update():
    """Test `merge` with nest dict-dict shallow->shallow/deep."""
    merged = merge(  {"a": {"aa": 1, "AA": 3}},
                     {"a": {         "AA": 2}})
    assert merged == {"a": {"aa": 1, "AA": 2}}


def test_merge_nest_child_partial_new():
    """Test `merge` with nest dict-dict shallow->deep/shallow."""
    merged = merge(  {"a": {"aa": 1,        }},
                     {"a": {"aa": 2, "AA": 2}})
    assert merged == {"a": {"aa": 2, "AA": 2}}
#### /Dict-Dict ########################################################################


def test_merge_list_dict():
    """Test `merge` with heterogeneous-nest, dict in list."""
    merged = merge(  [{"a": 1}, {"b": 3}, {"a": 2, "b": 2},],
                     [{"a": 2}, {"b": 2}, {"a": 1,       },],)
    assert merged == [{"a": 2}, {"b": 2}, {"a": 1, "b": 2},]


def test_merge_list_dict_list():
    """Test `merge` with heterogeneous-nest, list in dict in list."""
    merged = merge(  [{"a": [1, 1, 3]}, {"b": [1, {"c": 1}]}],
                     [{"a": [2, 2, 5]}, {"b": [2, {"c": 2}]}],)
    assert merged == [{"a": [2, 2, 5]}, {"b": [2, {"c": 2}]}]


def test_merge_instance_dict():
    """Test `merge` with class template."""

    @dataclass
    class Child:
        "Child"
        attr4: int  = 0
        attr5: bool = False

    @dataclass
    class ClsTest:
        """Root class"""
        attr1:      int         = 1
        attr2:      str         = "one"
        child:      Child       = default(Child(1, False))
        childlen_e: list[Child] = default([Child(attr4=1, attr5=True), Child(attr4=0, attr5=True)])
        childlen_t: list[Child] = default([Child(attr4=1, attr5=True)])

    conf = {
        "attr1": 2,
        "child": {
            "attr5": True
        },
        "childlen_e": [{},            {"attr5": False}],
        "childlen_t": [{},            {"attr4": 0},   {"attr5": False}, {"attr4": 0, "attr5": False}],
    }

    ground_truth = ClsTest(
        attr1 = 2,
        attr2 = "one",
        child = Child(
            attr4 = 1,
            attr5 = True),
        childlen_e = [Child(1, True), Child(0, False)],
        childlen_t = [Child(1, True), Child(0, True), Child(1, False),  Child(0, False)],
    )

    merged = merge(ClsTest(), conf)
    print("merged", merged)
    print("gt", ground_truth)
    assert merged == ground_truth
