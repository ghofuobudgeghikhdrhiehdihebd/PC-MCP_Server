from tools.base_tool import baseTool
from tools.tool_utils import resolve_to_absolute_path

class write(baseTool):
    def __init__(self):
        super().__init__(
            name="write",
            description="Writes to a file.",
            mandatory_args={"file_path", "content"},
            arg_descriptions={"file_path": "The path to the file to be written to.", "content": "The content to write to the file."},
        )

    async def execute(self, args: dict[str, str]) -> str:
        await super().execute(args)
        file_path = resolve_to_absolute_path(args["file_path"])
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(args["content"])
        return f"Successfully wrote {len(args['content'])} characters to {file_path}."