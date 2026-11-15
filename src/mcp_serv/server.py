from .tools.read import read
from .tools.write import write
from .tools.shell import shell
from .tools.tool_types import *

async def handle_request(request: ToolRequest) -> ToolResultSuccess | ToolResultError:
    tool_type = request.tool
    tool_args = request.params
    match tool_type:
        case "read":
            tool = read()
        case "write":
            tool = write()
        case "shell":
            tool = shell()
        case _:
            return ToolResultError("error", f"Invalid tool type, must be read, write, or shell. Got {tool_type}")
    try:
        tool_response = await tool.execute(tool_args)
        return ToolResultSuccess("success", tool_response)
    except Exception as e:
        return ToolResultError("error", f"Error executing tool: {str(e)}")