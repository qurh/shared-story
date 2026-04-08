from importlib import import_module
from types import ModuleType


def load_runtime_config(module_path: str = "config.phase1_runtime") -> ModuleType:
    return import_module(module_path)
