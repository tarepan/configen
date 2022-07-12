"""Configuration loader generation"""


from dataclasses import dataclass

from omegaconf import MISSING, SI

from .generate import generate_conf_loader


@dataclass
class _ChildChildConf:
    """Child of Child"""
    confcc1: str = MISSING

@dataclass
class _ChildConf:
    """Child"""
    confc1: str = MISSING
    confc2: int = MISSING
    confc3: _ChildChildConf = _ChildChildConf()

@dataclass
class _GlobalConf:
    """Root"""
    conf1: str = MISSING
    conf2: int = MISSING
    conf3: _ChildConf = _ChildConf(
        confc2=SI("${..conf2}"),)

def test_config():
    """Test config generated by loader-generator."""

    default_conf_str = """
    conf1: hello
    conf2: 3
    conf3:
        confc1: theChild
        confc3:
            confcc1: "${conf1}"
    """

    load_conf = generate_conf_loader(default_conf_str, _GlobalConf)
    conf = load_conf()
    assert conf.conf1 == "hello"
    assert conf.conf2 == 3
    assert conf.conf3.confc1 == "theChild"
    assert conf.conf3.confc2 == 3
    assert conf.conf3.confc3.confcc1 == "hello"
