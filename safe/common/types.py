import enum


class StrEnum(enum.Enum):
    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self.value)


@enum.unique
class RootCommand(StrEnum):
    """
    The types of commands that one can run with safe. For each
    command below, one can run

        safe COMMAND args-for-command

    Or:

        safe COMMAND --help

    to figure out their structure. Note that commands are
    lowercase, not uppercase.
    """
    CONVERT = "convert"
    CONFIG = "config"
    SHELL = "shell"
