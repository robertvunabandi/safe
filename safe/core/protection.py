import hashlib

from safe.common.constants import ENCODING
from safe.common.store import Store, StoreKey


def check_password(password: str) -> bool:
    hash_object = hashlib.sha512()
    hash_object.update(password.encode(ENCODING))
    given_hash = hash_object.hexdigest()
    expected_hash = Store.get(StoreKey.PASSWORD_HASH)
    return given_hash == expected_hash
