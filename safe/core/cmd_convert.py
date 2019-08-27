import pathlib
from safe.common import exit_codes
from safe.core.converter import Converter


def run(converter: Converter, filepath: pathlib.Path, decrypt: bool) -> int:
    # todo: write a function for this. should think about how
    #  this would fit with vim and other commands
    if not filepath.exists():
        # todo - better handle this with error messages,
        #  like a RunResult thing
        return exit_codes.FILE_DOES_NOT_EXIST
    raise NotImplementedError
