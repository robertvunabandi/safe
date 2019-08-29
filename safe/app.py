import sys
from pathlib import Path

from safe.common import exit_codes
from safe.common.types import RootCommand
from safe.core import cmd_config, cmd_convert, cmd_shell, parser, protection
from safe.core.converter import Converter


def run() -> None:
    args = sys.argv[1:]
    namespace = parser.parse_arguments(args)
    print(namespace)

    password = namespace.password
    if not protection.check_password(password):
        print("\nThe password you entered is invalid.\n")
        sys.exit(exit_codes.INVALID_PASSWORD)

    converter = Converter(password)

    # handle convert
    if namespace.safe_command == RootCommand.CONVERT:
        print("CONVERT")
        filepath = namespace.file
        should_decrypt = namespace.decrypt
        should_overwrite = namespace.overwrite
        name = namespace.name
        exit_code = cmd_convert.run(
            converter, Path(filepath), should_decrypt, should_overwrite, name
        )
        sys.exit(exit_code)

    # handle config
    if namespace.safe_command == RootCommand.CONFIG:
        print("CONFIG")
        data = cmd_config.ConfigData(new_password=namespace.new_password)
        exit_code = cmd_config.run(converter, data)
        sys.exit(exit_code)

    # handle shell
    if namespace.safe_command == RootCommand.SHELL:
        print("SHELL")
        filepath = namespace.safe_file
        cmd, cmd_args = namespace.command[0], namespace.command[:1]
        exit_code = cmd_shell.run(converter, filepath, cmd, *cmd_args)
        sys.exit(exit_code)
