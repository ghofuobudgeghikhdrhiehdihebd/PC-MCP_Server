import fastapi
import pjrpc
import uvicorn
from errors import *
from tools.read import read
from tools.write import write
from tools.shell import shell

app = fastapi.FastAPI()

# TODO: figure out how the hell to connect this up to the pi

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
            return pjrpc.Response(id=request.id, error=ToolNotFoundError(request.method))
    try:
        if request.params is None:
            request.params = {}
        output = await tool.execute(request.params)
        return pjrpc.Response(id=request.id, result=output)
    except AssertionError as e:
        print(str(e))
        return pjrpc.Response(id=request.id, error=BadRequestError())
    except FileNotFoundError as e:
        print(str(e))
        return pjrpc.Response(id=request.id, error=NonexistentFileError(request.params["file_path"]))
    except PermissionError as e:
        print(str(e))
        return pjrpc.Response(id=request.id, error=PermissionDeniedError())
    except Exception as e:
        print(str(e))
        return pjrpc.Response(id=request.id, error=UnknownError())

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)