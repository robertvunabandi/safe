import argparse
import getpass
from typing import Callable, List, Type

from safe.common.types import RootCommand


_SUPPORTED_COMMANDS = [
    "cat",
    "grep",
    "vi",
    "vim",
]
_ERROR_KEY = "safe_error"


def _password_action(prompt: str = "Password: ") -> Type[argparse.Action]:

    class PasswordPromptAction(argparse.Action):
        """
        This Action forces the user to provide a password safely
        after they enter all parameters.
        """

        def __init__(
            self, option_strings: str, dest: str, nargs: int = 0, **kwargs
        ) -> None:
            if nargs != 0:
                raise RuntimeError(
                    "Anything other than 0 is not allowed for "
                    "PasswordPromptAction"
                )
            super(PasswordPromptAction, self).__init__(
                option_strings, dest, nargs, **kwargs
            )

        def __call__(  # type: ignore
            self,
            parser: argparse.ArgumentParser,
            args: argparse.Namespace,
            values: List[str],
            option_string: str = None,
        ) -> None:
            password = getpass.getpass(prompt=prompt)
            setattr(args, self.dest, password)

    return PasswordPromptAction


class _CommandValidatorAction(argparse.Action):
    """
    Specifically created for checking whether the command entered
    is one the _SUPPORTED_COMMANDS when given a `shell` command
    """

    def __init__(self, option_strings, dest, nargs="+", **kwargs):
        super(_CommandValidatorAction, self).__init__(
            option_strings, dest, nargs, **kwargs
        )

    def __call__(  # type: ignore
        self,
        parser: argparse.ArgumentParser,
        args: argparse.Namespace,
        values: List[str],
        option_string: str = None,
    ) -> None:
        supported = self.const
        command = values[0]
        if command not in supported:
            error = (
                f"Command `{command}` is not supported. Please "
                f"use one of (`{'`, `'.join(supported)}`)."
            )
            setattr(args, _ERROR_KEY, error)
        setattr(args, self.dest, values)


def _safe_command_setter_action(
    action: RootCommand
) -> Callable[..., argparse.Action]:
    class SafeActionSetterAction(argparse.Action):
        def __call__(  # type: ignore
            self,
            parser: argparse.ArgumentParser,
            args: argparse.Namespace,
            values: List[str],
            option_string: str = None,
        ) -> None:
            setattr(args, self.dest, action)

    return SafeActionSetterAction


def _set_parser_command(
    parser: argparse.ArgumentParser, action: RootCommand
) -> None:
    """
    Adds a silent argument that sets the action for this parser.
    This is because different actions lead to different steps to
    take given the arguments of the parser.

    :param parser: parser
    :param action: action to set
    """
    parser.add_argument(  # type: ignore
        "safe_command",
        nargs=0,
        action=_safe_command_setter_action(action),
        type=RootCommand,
        help=argparse.SUPPRESS,
    )


def _add_password_argument(parser: argparse.ArgumentParser) -> None:
    """
    Adds a password argument to the parser parser. This password
    argument is silent such that it's not even visible when client
    calls the parser with arguments `--help`. This password argument
    is also always required.
    """
    parser.add_argument(
        "password",
        nargs=0,
        action=_password_action(),
        type=str,
        help=argparse.SUPPRESS,
    )


def _get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "An application to encrypt/decrypt files and run "
            "programs on encrypted `.safe` files. All accesses "
            "to this program are guarded by a password, which "
            "is set by the main user of this machine. This "
            "password is then used to encrypt and decrypt files."
        ),
        prog="safe",
    )
    subparsers = parser.add_subparsers(
        title="Available commands",
        description=(
            "These are the available commands that can be used "
            "in this command line argument application."
        ),
        help="Available commands",
    )

    # convert: converting a file from `.ext` to/from `.ext.safe`

    convert_cmd = subparsers.add_parser(
        "convert", help="Encryption/decryption of files"
    )
    _set_parser_command(convert_cmd, RootCommand.CONVERT)
    convert_cmd.add_argument(
        dest="file",
        metavar="FILE",
        help=(
            "file to encrypt/decrypt. This is a file to "
            "encrypt by default."
        ),
    )
    convert_cmd.add_argument(
        "-d",
        "--decrypt",
        dest="decrypt",
        action="store_true",
        default=False,
        help=(
            "whether the file given is a `.safe` file that "
            "is meant to be decrypted."
        ),
    )
    _add_password_argument(convert_cmd)

    # config: configurations, like password and salt

    config_cmd = subparsers.add_parser(
        "config", help="Configuration settings for the `safe` application"
    )
    _set_parser_command(config_cmd, RootCommand.CONFIG)
    config_cmd.add_argument(
        "-sp",
        "--set-password",
        dest="new_password",
        action=_password_action("New Password: "),
        type=str,
        required=False,
        help=(
            "whether to set or reset the password. This will "
            "re-encrypt all previously encrypted files, which may "
            "take a while depending on how many files there are."
        ),
    )
    _add_password_argument(config_cmd)

    # shell: running other unix commands on `.safe` files

    shell_cmd = subparsers.add_parser(
        "shell", help="Run a shell command with a `.safe` file"
    )
    _set_parser_command(shell_cmd, RootCommand.SHELL)
    shell_cmd.add_argument(
        dest="safe_file",
        metavar="FILE",
        help="`.safe` file on which to run a shell command",
    )
    shell_cmd.add_argument(
        "-cmd",
        "--command",
        dest="command",
        metavar=("COMMAND", "ARG"),
        nargs=argparse.ONE_OR_MORE,
        help="shell command to run on `.safe` file. E.g., `-cmd vi`",
        const=_SUPPORTED_COMMANDS,
        action=_CommandValidatorAction,
        required=True,
    )
    _add_password_argument(shell_cmd)

    return parser


def _has_attribute(namespace: argparse.Namespace, attr: str) -> bool:
    """
    Returns True if the namespace has a Non-None value for the given
    attribute. False otherwise.
    """
    return hasattr(namespace, attr) and getattr(namespace, attr) is not None


def parse_arguments(args: List[str]) -> argparse.Namespace:
    """
    Parses the arguments and returns the appropriate namespace. This
    exits with an error in case there is an error in the arguments
    given.
    :return
        a namespace that has a field `safe_command` indicating which
        command was run. See above for the attributes of the namespace
        given the command.
    """
    parser = _get_parser()
    ns = parser.parse_args(args)

    if hasattr(ns, _ERROR_KEY) and getattr(ns, _ERROR_KEY) is not None:
        parser.error(ns.error)

    return ns
