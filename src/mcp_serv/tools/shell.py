from pjrpc.common import JsonT
from .load_tool import load_tool
from .base_tool import baseTool
import asyncio

class shell(baseTool):
    def __init__(self):
        super().__init__(load_tool("shell"))

    async def execute(self, args: dict[str, JsonT]) -> str:
        await super().execute(args)
        command = args["command"]
        timeout = int(args.get("timeout", 30))
        try:
            process = await asyncio.create_subprocess_shell(
                "cd && " + command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            out, err = await asyncio.wait_for(process.communicate(), timeout=timeout)
            return out.decode() if process.returncode == 0 else err.decode()
        except asyncio.TimeoutError:
            return f"Command '{command}' timed out after {timeout} seconds."