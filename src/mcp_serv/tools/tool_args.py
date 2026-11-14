from dataclasses import dataclass

@dataclass
class ToolArgs:
    """
    A dataclass that represents the arguments for a tool.
    """
    name: str
    description: str
    required_args: set[str]
    optional_args: set[str] | None
    arg_descriptions: dict[str, str]