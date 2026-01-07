import os
from dataclasses import dataclass
from typing import Literal

Environment = Literal["dev", "staging", "prod"]
Mode = Literal["raise", "log", "silent"]

@dataclass
class Config:
    env: Environment = "dev"
    sample_size: float = 1.0
    mode:  Mode = "raise"


    def __post_init__(self):
        """Validating config values"""
        if not 0.0 <= self.sample_size<= 1.0:
            raise ValueError("Sample must be between 0.0 and 1.0")
        if self.env not in ["dev","staging","prod"]:
            raise ValueError("Environment must be 'dev', 'staging', or 'prod'")
        if self.mode not in ["raise","log","silent"]:
            raise ValueError("Mode must be 'raise', 'log', or 'silent'")
        


_config = Config(
    env=os.getenv("PY_FLOWCHECK_ENV", "dev"),
    sample_size=float(os.getenv("PY_FLOWCHECK_SAMPLE_SIZE", "1.0")),
    mode=os.getenv("PY_FLOWCHECK_MODE", "raise")
)


def configure(
        env: Environment = None,
        sample_size: float = None,
        mode: Mode = None   

) -> None:
    """Configure the global settings for py_flowcheck."""
    global _config
    if env is not None:
        _config.env = env
    if sample_size is not None:
        _config.sample_size = sample_size
    if mode is not None:
        _config.mode = mode
    _config.__post_init__()


def get_config() -> Config:
    """Getting  the current global configuration for the py_flowcheck."""
    return _config    
