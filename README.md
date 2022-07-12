# configen
OmegaConf-Config Generator

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
