import pathlib
from safe.common import exit_codes
from safe.core.converter import Converter


def run(converter: Converter, filepath: pathlib.Path, decrypt: bool) -> None:
    # todo: write a function for this. should think about how
    #  this would fit with vim and other commands
    if not filepath.exists():
        # todo - better handle this with exit codes
        raise ValueError("File doesn't exist") 
    raise NotImplementedError
