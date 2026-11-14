from pjrpc.common import JsonT
from .base_tool import baseTool
from .load_tool import load_tool
from .tool_utils import resolve_to_absolute_path

class read(baseTool):
    def __init__(self):
        super().__init__(load_tool("read"))

    async def execute(self, args: dict[str, JsonT]) -> str:
        await super().execute(args)
        file_path = resolve_to_absolute_path(args["file_path"])
        max_length = int(args.get("max_length", 1000))
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()[:max_length]