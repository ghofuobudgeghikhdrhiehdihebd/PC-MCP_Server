from abc import ABC, abstractmethod

class baseTool(ABC):
    def __init__(self, name: str, description: str, mandatory_args: set[str], arg_descriptions: dict[str, str], optional_args: set[str] | None = None):
        self.name = name
        self.description = description
        self.mandatory_args = mandatory_args
        self.optional_args = optional_args if optional_args is not None else set()
        self.args = mandatory_args | self.optional_args
        assert(self.args == set(arg_descriptions.keys())), f"Argument descriptions must match the provided arguments. Expected: {self.args}, but got: {set(arg_descriptions.keys())}"
        self.arg_descriptions = arg_descriptions

    def assert_args(self, args: dict[str, str]):
        for arg in self.mandatory_args:
            assert arg in args, f"Missing mandatory argument: {arg}"
        for provided_arg in args.keys():
            assert provided_arg in self.args, f"Unexpected argument: {provided_arg}"

    @abstractmethod
    async def execute(self, args: dict[str, str]) -> str:
        # check if args are valid (all mandatory provided, no unexpected provided)
        self.assert_args(args)