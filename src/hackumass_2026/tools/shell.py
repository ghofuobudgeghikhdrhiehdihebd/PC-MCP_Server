from tools.base_tool import baseTool
import asyncio

class shell(baseTool):
    def __init__(self):
        super().__init__(
            name="execute",
            description="Executes a command and returns its output.",
            mandatory_args={"command"},
            optional_args={"timeout"},
            arg_descriptions={"command": "The command to be executed.", "timeout": "The maximum time to wait for the command to complete (default: 30 seconds)"},
        )

    async def execute(self, args: dict[str, str]) -> str:
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