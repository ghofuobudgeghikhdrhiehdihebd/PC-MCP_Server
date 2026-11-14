import json
from .tool_args import ToolArgs

with open("src/mcp_serv/tools/tools.json", "r") as f:
    tools = json.load(f)

def load_tool(name: str) -> ToolArgs:
    if name not in tools:
        raise ValueError(f"Tool '{name}' not found in tools.json")
    tool = tools[name]
    args = tool["params"]
    mandatory = set()
    optional = set()
    descriptions = {}
    for arg, data in args.items():
        if data["mandatory"]:
            mandatory.add(arg)
        else:
            optional.add(arg)
        descriptions[arg] = data.get("description", "")
    return ToolArgs(
        name=name,
        description=tool["description"],
        required_args=mandatory,
        optional_args=optional,
        arg_descriptions=descriptions
    )