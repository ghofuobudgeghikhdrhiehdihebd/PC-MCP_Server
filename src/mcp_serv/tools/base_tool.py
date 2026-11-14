from abc import ABC, abstractmethod
from pjrpc.common import JsonT
from .tool_args import ToolArgs

class baseTool(ABC):
    def __init__(self, args: ToolArgs):
        self.name = args.name
        self.description = args.description
        self.mandatory_args = args.required_args
        self.optional_args = args.optional_args if args.optional_args is not None else set()
        self.args = args.required_args | self.optional_args
        print(f"Initializing tool: {self.name}")
        print(f"Mandatory args: {self.mandatory_args}")
        print(f"Optional args: {self.optional_args}")
        assert(self.args == set(args.arg_descriptions.keys())), f"Argument descriptions must match the provided arguments. Expected: {self.args}, but got: {set(args.arg_descriptions.keys())}"
        self.arg_descriptions = args.arg_descriptions

    def assert_args(self, args: dict[str, JsonT]):
        for arg in self.mandatory_args:
            assert arg in args, f"Missing mandatory argument: {arg}"
        for provided_arg in args.keys():
            assert provided_arg in self.args, f"Unexpected argument: {provided_arg}"

    @abstractmethod
    async def execute(self, args: dict[str, JsonT]) -> JsonT:
        # check if args are valid (all mandatory provided, no unexpected provided)
        self.assert_args(args)