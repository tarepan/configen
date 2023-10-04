"""Merge."""

from typing import Any
from dataclasses import asdict
from copy import deepcopy
import warnings


primitives = (type(None), bool, int, float, str)


# [Design Notes]
# usecase:
#     - Merge two partial configs: config file & CLI (basically primitive/tuple/list/dict merge, rarely instance merge)
#     - Merge instance and config: Config class instance & CLI (Mainly instance-dict merge)

none_type = type(None)

def merge(base: Any, another: Any) -> Any:
    """Merge two objects.

    Rules:
        - special
            - reference
                - ref precedence: (a & ref) | (ref & a) -> ref
        - homogenous
            - primitive
                - Reassignment: a & b -> b
            - tuple
                - Element-wise merge: (a1, a2, a3) & (b1, b2, b3) -> (merge(a1,b1), merge(a2,b2), merge(a3,b3))
            - list
                - Element-wise merge: [a1, a2, a3] & [b1, b2, b3] -> [merge(a1,b1), merge(a2,b2), merge(a3,b3)]
                - Template expansion: [t]          & [b1, b2, b3] -> [merge(t, b1), merge(t, b2), merge(t, b3)]
            - dict
                - non-conflict expansion & conflict merge: {a:A, c:C1} & {b:B, c:C2} -> {a:A, b:B, c:merge(C1,C2)}
            - instance
                - attribute-wise merge: C(x1,y1) & C(x2,y2) -> C(merge(x1,x2),merge(y1,y2))
        - heterogenous
            - null/any and any/null
                - Reassignment: a & b (a=null|b=null) -> b
            - instance/dict
                - conflict merge: C(x=x1,y=y1) & {x:x2} -> C(x=merge(x1,x2),y=y1)

    Args:
        base    - Base object
        another - Another object, which may override the base
    """

    type_base, type_another = type(base), type(another)

    # Special
    ## Reference
    if (type_base    is str) and (   base[:2] == "${" and    base[-1] == "}"):
        raise RuntimeError("Overriding reference is prohibited.")
        # return base
    if (type_another is str) and (another[:2] == "${" and another[-1] == "}"):
        return another
    ## Missing
    if base == "???":
        return another

    # Homogenous
    if type_base is type_another:
        if type_base in primitives:
            return another
        if type_base is tuple:
            return merge_tuple(base, another)
        if type_base is list:
            return merge_list(base, another)
        if type_base is dict:
            return merge_dict(base, another)
        # Class instance
        return merge_instance(base, another)

    # Heterogenous
    ## Null-Any | Any-Null
    if (type_base is none_type) or (type_another is none_type):
        return deepcopy(another)
    ## Instance-Dict
    if type_base not in (primitives + (tuple, list, dict)):
        if type_another is dict:
            return merge_instance_dict(base, another)
    raise RuntimeError(f"Heterogenous merge is permitted only in Instance-Dict, but {type_base}-{type_another}; {str(base)}-{str(another)}.")


def merge_tuple(base: tuple[Any], another: tuple[Any]) -> tuple[Any]:
    """Merge two tuples.

    Rules:
        - Element-wise merge: (a1, a2, a3) & (b1, b2, b3) -> (merge(a1,b1), merge(a2,b2), merge(a3,b3))

    Args:
        base    - Base    tuple, L=l
        another - Another tuple, L=l
    Returns:
                - Merged  tuple, L=l
    """

    if len(base) == len(another):
        return tuple(merge(base_i, another_i) for base_i, another_i in zip(base, another))

    # L_base != L_another
    raise RuntimeError(f"Tuple merge support only Element-wise, but base length {len(base)} != another length {len(another)}.")


def merge_list(base: list[Any], another: list[Any]) -> list[Any]:
    """Merge two lists.

    Rules:
        - Element-wise merge: [a1, a2, a3] & [b1, b2, b3] -> [merge(a1,b1), merge(a2,b2), merge(a3,b3)]
        - Template expansion: [t]          & [b1, b2, b3] -> [merge(t, b1), merge(t, b2), merge(t, b3)]
        - Whole reassignment: [a1, a2]     & [b1, b2, b3] -> [b1, b2, b3]

    Args:
        base    - Base list (L>1) OR template in list (L==1)
        another - Another list (L>0)
    Returns:
                - Merged list
    """
    # Template expansion
    if len(base) == 1:
        return [merge(base[0], another_i) for another_i in another]

    # Element-wise merge
    if len(base) == len(another):
        return [merge(base_i, another_i) for base_i, another_i in zip(base, another)]

    # Whole-list reassignment
    warnings.warn(f"Non-matched length {len(base)} & {len(another)} is given. Whole list is replaced/reassignment")
    return another


def merge_dict(base: dict[str, Any], another: dict[str, Any]) -> dict[str, Any]:
    """Merge two dictionaries.
    
    Rules:
        - non-conflict expansion & conflict merge: {a:A, c:C1} & {b:B, c:C2} -> {a:A, b:B, c:merge(C1,C2)}
    """
    # Expansion
    merged = {**deepcopy(base), **deepcopy(another)}
    # Conflict merge
    for k, v_base in base.items():
        if k in another:
            merged[k] = merge(v_base, another[k])
    return merged


def merge_instance(base: Any, another: Any) -> Any:
    """Merge two instances."""
    merged = deepcopy(base)
    for k, v_another in asdict(another).items():
        v_base = getattr(base, k)
        setattr(merged, k, merge(v_base, v_another))
    return merged


def merge_instance_dict(base: Any, another: dict[str, Any]) -> Any:
    """Merge a dictionary `another` into a class instance `base`."""
    merged = deepcopy(base)
    for k, v_another in another.items():
        v_base = getattr(base, k)
        setattr(merged, k, merge(v_base, v_another))
    return merged
