import re
from pathlib import Path
from typing import Union

from safe.common import exit_codes
from safe.core.converter import Converter


def run(converter: Converter, filepath: Path, decrypt: bool) -> int:
    if not filepath.exists():
        # todo - somehow print error messages to tell that the file doesn't exist
        return exit_codes.FILE_DOES_NOT_EXIST
    if decrypt:
        return _run_decryption(converter, filepath)
    return _run_encryption(converter, filepath)


def _run_encryption(converter: Converter, filepath: Path) -> int:
    with filepath.open("r") as f:
        lines = f.read().splitlines()
        encrypted_lines = converter.encrypt_lines(lines)
        encrypted_fpath = Path(f"{str(filepath)}.safe")
        try:
            _store_content_into_path(encrypted_fpath, encrypted_lines)
        except ValueError as ve:
            print(f"An error occurred:\n{ve}")
            return exit_codes.CONVERSION_FAILED
        return exit_codes.SUCCESS


def _run_decryption(converter: Converter, filepath: Path) -> int:
    if not filepath.name.endswith(".safe"):
        return exit_codes.FILE_IS_NOT_SAFE_FILE
    with filepath.open("rb") as f:
        lines = f.read().splitlines()
        decrypted_lines = converter.decrypt_lines(lines)
        decrypted_fpath = filepath.with_name(filepath.stem)
        try:
            _store_content_into_path(decrypted_fpath, decrypted_lines)
        except ValueError as ve:
            print(f"An error occurred:\n{ve}")
            return exit_codes.CONVERSION_FAILED
        return exit_codes.SUCCESS


def _store_content_into_path(
    decrypted_fpath: Path, content: Union[bytes, str], overwrite: bool = False
) -> None:
    if not decrypted_fpath.exists() or overwrite:
        file_flag = "wb" if type(content) == bytes else "w"
        with decrypted_fpath.open(file_flag) as df:
            if overwrite:
                df.truncate(0)
            df.write(content)
        return
    raise ValueError("Cannot overwrite content of the file.")
