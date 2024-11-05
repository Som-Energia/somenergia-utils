from .pathlib import Path
from yamlns import namespace as ns


def _load_module(module_name, module_path):
    try:
        # Py2 version
        import imp
        return imp.load_source(module_name, module_path)
    except ImportError:
        # Py3 version
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


def load_py_config(file):
    file = Path(file)

    module_name = file.stem
    module_path = str(file)

    module = _load_module(module_name, module_path)

    return ns((
        (key, val)
        for key, val in module.__dict__.items()
        if not key.startswith("_")
    ))
