# configen
Config Generator, like OmegaConf.

## Install
```bash
pip install git+https://github.com/tarepan/configen.git
```

## Usage
```python
from configen import generate_conf_loader

conf_dataclass = ...
default_str = "..."

# Exported
load_conf = generate_conf_loader(default_str, conf_dataclass)
"""Load configuration type-safely.
"""
```

## Merge rules
- Rules:
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
