"""Configuration loader generation"""

from typing import Callable, TypeVar

from omegaconf import OmegaConf, SCMode

from .merge import merge


T = TypeVar('T') # dataclass
def generate_conf_loader(default_str: str, conf_class: T) -> Callable[[], T]:
    """Generate 'Load configuration type-safely' function.
    Priority: CLI args > CLI-specified config yaml > Default
    """

    def load_configuration() -> T:
        """Load configurations."""

        # Instantiation
        default_dict    = OmegaConf.to_container(OmegaConf.create(default_str))
        cli_dict        = OmegaConf.to_container(OmegaConf.from_cli())
        extends_path = cli_dict.get("path_extend_conf", None)
        if extends_path:
            extend_dict = OmegaConf.to_container(OmegaConf.load(extends_path))

        # Merge
            conf_unresolved = merge(conf_class(), merge(merge(default_dict, extend_dict), cli_dict))
        else:
            conf_unresolved = merge(conf_class(), merge(default_dict, cli_dict))

        # Interpolation
        conf_structured = OmegaConf.structured(conf_unresolved)
        OmegaConf.resolve(conf_structured)

        # Design Note -- OmegaConf instance v.s. DataClass instance --
        #   OmegaConf instance has runtime overhead in exchange for type safety.
        #   Configuration is constructed/finalized in early stage,
        #   so config is eternally valid after validation in last step of early stage.
        #   As a result, we can safely convert OmegaConf to DataClass after final validation.
        #   This prevent (unnecessary) runtime overhead in later stage.
        #
        #   One demerit: No "freeze" mechanism in instantiated dataclass.
        #   If OmegaConf, we have `OmegaConf.set_readonly(conf_final, True)`

        # Validation
        return OmegaConf.to_container(conf_structured, structured_config_mode=SCMode.INSTANTIATE) # type: ignore ; It is validated by omegaconf

    return load_configuration
