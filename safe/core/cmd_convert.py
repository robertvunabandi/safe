from pathlib import Path
from typing import Optional, Union

from safe.common import exit_codes
from safe.core.converter import Converter


def run(
    converter: Converter,
    filepath: Path,
    decrypt: bool,
    overwrite: bool = False,
    name: Optional[str] = None,
) -> int:
    if not filepath.exists():
        # todo - somehow print error messages to tell that the file doesn't exist
        return exit_codes.FILE_DOES_NOT_EXIST
    if decrypt:
        return _run_decryption(converter, filepath, overwrite, name)
    return _run_encryption(converter, filepath, overwrite, name)


def _run_encryption(
    converter: Converter, filepath: Path, overwrite: bool, name: Optional[str] = None
) -> int:
    with filepath.open("r") as f:
        lines = f.read().splitlines()
        encrypted_lines = converter.encrypt_lines(lines)
        if name is not None:
            name = name if name.endswith(".safe") else f"{name}.safe"
        encrypted_fpath = (
            filepath.with_suffix(".safe")
            if name is None
            else filepath.with_name(name)
        )
        try:
            _store_content_into_path(encrypted_fpath, encrypted_lines, overwrite)
        except ValueError as ve:
            print(f"An error occurred:\n{ve}")
            return exit_codes.CONVERSION_FAILED
        return exit_codes.SUCCESS


def _run_decryption(
    converter: Converter, filepath: Path, overwrite: bool, name: Optional[str] = None
) -> int:
    if not filepath.name.endswith(".safe"):
        return exit_codes.FILE_IS_NOT_SAFE_FILE
    with filepath.open("rb") as f:
        lines = f.read().splitlines()
        decrypted_lines = converter.decrypt_lines(lines)
        if name is not None:
            if name.endswith(".safe"):
                print(f"The name given ({name}) cannot have the `.safe` extension.")
                return exit_codes.CONVERSION_FAILED
        decrypted_fpath = (
            filepath.with_name(filepath.stem)
            if name is None
            else filepath.with_name(name)
        )
        try:
            _store_content_into_path(decrypted_fpath, decrypted_lines, overwrite)
        except ValueError as ve:
            print(f"An error occurred:\n{ve}")
            return exit_codes.CONVERSION_FAILED
        return exit_codes.SUCCESS


def _store_content_into_path(
    decrypted_fpath: Path, content: Union[bytes, str], overwrite: bool
) -> None:
    if not decrypted_fpath.exists() or overwrite:
        file_flag = "wb" if type(content) == bytes else "w"
        with decrypted_fpath.open(file_flag) as df:
            if overwrite:
                df.truncate(0)
            df.write(content)
        return
    raise ValueError("Cannot overwrite content of the file.")
