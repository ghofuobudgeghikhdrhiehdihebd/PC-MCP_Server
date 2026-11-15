import fastapi
from fastapi import Request, Response
import uvicorn
from .tools.read import read
from .tools.write import write
from .tools.shell import shell

app = fastapi.FastAPI()

@app.post("/")
async def handle_request(request: Request) -> Response:
    req_json = await request.json()
    request_type = req_json.get("type", "")
    if (request_type != "tool_call"):
        return Response(
            content={
                "status": "failure",
                "error": "Invalid request type, must be 'tool_call'"
            },
            media_type="application/json",
            status_code=400,
        )
    tool_type = req_json.get("tool", "")
    tool_args = req_json.get("params", {})
    match tool_type:
        case "read":
            tool = read()
        case "write":
            tool = write()
        case "shell":
            tool = shell()
        case _:
            return Response(
                content={
                    "status": "failure",
                    "error": 'Invalid tool type, must be read, write, or shell'
                },
                media_type="application/json",
                status_code=400,
            )
    try:
        tool_response = await tool.execute(tool_args)
        return Response(
            content={
                "status": "success",
                "result": tool_response
            },
            media_type="application/json",
            status_code=200,
        )
    except Exception as e:
        return Response(
            content={
                "status": "failure",
                "error": f"Error executing tool: {str(e)}"
            },
            media_type="application/json",
            status_code=500,
        )

if __name__ == "__main__":
    # run as UDS, not HTTP
    uvicorn.run(app, uds="/tmp/mcp_serv.sock")