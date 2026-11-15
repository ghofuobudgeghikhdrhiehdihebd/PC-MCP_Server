import fastapi
from fastapi.responses import JSONResponse
import pjrpc
from .errors import *
from .tools.read import read
from .tools.write import write
from .tools.shell import shell

app = fastapi.FastAPI()

async def ret_ok(id: str, result):
    return JSONResponse(pjrpc.Response(id=id, result=result).to_json())

async def ret_error(id: str, error):
    return JSONResponse(pjrpc.Response(id=id, error=error).to_json())

@app.post("/")
async def handle_request(request: pjrpc.Request) -> pjrpc.Response:
    match request.method:
        case "read":
            tool = read()
        case "write":
            tool = write()
        case "shell":
            tool = shell()
        case _:
            return await ret_error(str(request.id), ToolNotFoundError(request.method))
    if not isinstance(request.params, dict):
        return await ret_error(str(request.id), BadRequestError())
    try:
        if request.params is None:
            request.params = {}
        output = await tool.execute(request.params)
        return await ret_ok(str(request.id), output)
    except AssertionError as e:
        print(str(e))
        return await ret_error(str(request.id), BadRequestError())
    except FileNotFoundError as e:
        if "file_path" not in request.params.keys():
            return await ret_error(str(request.id), BadRequestError())
        print(str(e))
        return await ret_error(str(request.id), NonexistentFileError(request.params["file_path"]))
    except PermissionError as e:
        print(str(e))
        return await ret_error(str(request.id), PermissionDeniedError())
    except Exception as e:
        print(str(e))
        return await ret_error(str(request.id), UnknownError())