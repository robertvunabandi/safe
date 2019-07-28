from typing import Sequence

from cryptography.fernet import Fernet  # type: ignore

from safe.common.constants import ENCODING

_KEY_LENGTH = 44


class Converter:
    def __init__(self, password: str) -> None:
        self.__fernet = Fernet(Converter._make_key(password))

    def encrypt_lines(self, lines: Sequence[str]) -> bytes:
        return b"\n".join(self.encrypt(line) for line in lines)

    def encrypt(self, line: str) -> bytes:
        return self.__fernet.encrypt(line)

    def decrypt_lines(self, lines: Sequence[bytes]) -> str:
        return "\n".join(self.decrypt(token) for token in lines)

    def decrypt(self, token: bytes) -> str:
        value: bytes = self.__fernet.decrypt(token)
        return value.decode(ENCODING)

    @staticmethod
    def _make_key(password: str) -> bytes:
        """
        Makes a key given the key source.
        :param password:
            the user's password
        :return:
            key to use for making the Fernet. Given the same password,
            this always returns the same key.
        """
        return Converter._extend(password).encode(ENCODING)

    @staticmethod
    def _extend(root: str) -> str:
        extended = root
        while len(extended) < _KEY_LENGTH:
            extended += extended[:_KEY_LENGTH - len(extended)]
        return extended[:_KEY_LENGTH - 1] + "="

