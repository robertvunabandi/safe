import os
from typing import Union

from safe.common.types import StrEnum


# todo: This path is temporary to work with. Eventually, we should
#  migrate to working with `appdirs` with either storing the key inside
#  whatever `appdirs` path we get or use sqlite to store things, but
#  still the DB would be inside the location provided through `appdirs`.
#  This change will lead to changing the execution of Store.get and
#  Store.set.
STORE_PATH = "store"


class StoreException(Exception):
    pass


class PasswordNotSetException(StoreException):
    pass


class PasswordSaltNotSetException(StoreException):
    pass


class UnknownStoreException(Exception):
    pass


class StoreKey(StrEnum):
    PASSWORD_HASH = "PASSWORD_HASH"


class Store:
    """
    Class to get store variables
    """

    # sets of keys that one can change
    _SETTABLE = {
        StoreKey.PASSWORD_HASH,
    }

    @staticmethod
    def get(key: StoreKey) -> str:
        try:
            with open(os.path.join(STORE_PATH, str(key)), "r") as f:
                return f.readline().lower()
        except FileNotFoundError:
            raise Store._get_exception(key)

    @staticmethod
    def set(key: StoreKey, value: str) -> None:
        if key not in Store._SETTABLE:
            raise ValueError(
                f"the key {key} is not allowed to be changed."
            )
        with open(os.path.join(STORE_PATH, str(key)), "w") as f:
            f.write(value.lower())

    @staticmethod
    def _get_exception(key: StoreKey) -> Union[StoreException, UnknownStoreException]:
        if key == StoreKey.PASSWORD_HASH:
            return PasswordNotSetException(
                "No password have been set yet. Please run\n\n"
                "  safe --set-password\n\n"
                "to set a password for files."
            )
        return UnknownStoreException(
            "Unknown error occurred. This is likely an internal "
            f"error with the application. Key given was {key}."
        )
