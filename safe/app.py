import sys

from safe.common import exit_codes
from safe.common.types import RootCommand
from safe.core import parser
from safe.core.converter import Converter
from safe.core import protection


def run() -> None:
    args = sys.argv[1:]
    namespace = parser.parse_arguments(args)
    print(namespace)

    password = namespace.password
    if not protection.check_password(password):
        print("\nThe password you entered is invalid.\n")
        exit(exit_codes.INVALID_PASSWORD)

    converter = Converter(password)

    # handle convert
    if namespace.safe_command == RootCommand.CONVERT:
        print("CONVERT")
        filepath = namespace.file
        should_decrypt = namespace.decrypt

        # todo: write a function for this. should think about how
        #  this would fit with vim and other commands
        if should_decrypt:
            # output = read_safe_file_and_decrypt(filepath, converter)
            pass
        else:
            # output = read_file_and_encrypt(filepath, converter)
            pass
        # print(output)
        exit(exit_codes.SUCCESS)

    # handle config
    if namespace.safe_command == RootCommand.CONFIG:
        print("CONFIG")
        new_password = namespace.new_password
        # todo: write a function for this. this function should
        #  first read all the encrypted files and decrypt them,
        #  then change the password, then re-encrypt the files.
        #  in addition, if it's stopped somewhere in the middle
        #  of doing all of that, nothing should be changed
        #  must also work for salt or both at the same time
        exit(exit_codes.SUCCESS)

    # handle shell
    if namespace.safe_command == RootCommand.SHELL:
        print("SHELL")
        filepath = namespace.safe_file
        cmd, cmd_args = namespace.command[0], namespace.command[:1]
        # todo: write this method
        exit(exit_codes.SUCCESS)
