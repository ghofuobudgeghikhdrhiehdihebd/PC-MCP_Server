from tools.base_tool import baseTool
from tools.tool_utils import resolve_to_absolute_path

class read(baseTool):
    def __init__(self):
        super().__init__(
            name="read",
            description="Reads a file and returns its contents.",
            mandatory_args={"file_path"},
            optional_args={"max_length"},
            arg_descriptions={"file_path": "The path to the file to be read.", "max_length": "The maximum number of characters to read (default: 1000)"},
        )

    async def execute(self, args: dict[str, str]) -> str:
        await super().execute(args)
        file_path = resolve_to_absolute_path(args["file_path"])
        max_length = int(args.get("max_length", 1000))
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()[:max_length]