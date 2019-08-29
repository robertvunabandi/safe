from safe.core.converter import Converter


def run(converter: Converter, filepath: str, command: str, *args: str) -> int:
    # todo: write a function for this. this function should
    #  first read all the encrypted files and decrypt them,
    #  then change the password, then re-encrypt the files.
    #  in addition, if it's stopped somewhere in the middle
    #  of doing all of that, nothing should be changed
    #  must also work for salt or both at the same time
    raise NotImplementedError
