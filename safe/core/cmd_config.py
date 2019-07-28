from typing import NamedTuple, Optional

from safe.core.converter import Converter


class ConfigData(NamedTuple):
    new_password: Optional[str]


def run(converter: Converter, data: ConfigData) -> None:
    # todo: write a function for this. this function should
    #  first read all the encrypted files and decrypt them,
    #  then change the password, then re-encrypt the files.
    #  in addition, if it's stopped somewhere in the middle
    #  of doing all of that, nothing should be changed (i.e.,
    #  this operation should be atomic).
    if data.new_password:
        raise NotImplementedError
