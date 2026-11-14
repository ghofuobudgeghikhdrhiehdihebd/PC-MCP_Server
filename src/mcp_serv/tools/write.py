from pjrpc.common import JsonT
from .load_tool import load_tool
from .base_tool import baseTool
from .tool_utils import resolve_to_absolute_path

class write(baseTool):
    def __init__(self):
        super().__init__(load_tool("write"))

    async def execute(self, args: dict[str, JsonT]) -> str:
        await super().execute(args)
        file_path = resolve_to_absolute_path(args["file_path"])
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(args["content"])
        return f"Successfully wrote {len(args['content'])} characters to {file_path}."