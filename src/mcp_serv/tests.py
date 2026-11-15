from .server import app
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
import pytest
import pjrpc
from pjrpc.common.exceptions import JsonRpcError

def json_rpc_response(response: pjrpc.Response) -> JSONResponse:
    return JSONResponse(content=response.to_json())

@pytest.fixture
def rpc_client():
    with TestClient(app) as client:

        def send(request: pjrpc.Request) -> pjrpc.Response:
            http_response = client.post(
                "/",
                json=request.to_json(),
            )

            assert http_response.status_code == 200

            if http_response.json().get("error") is not None:
                return pjrpc.Response(
                    id=request.id,
                    error=JsonRpcError(
                        code=http_response.json()["error"]["code"],
                        message=http_response.json()["error"]["message"],
                        data=http_response.json()["error"].get("data"),
                    )
                )
            else:
                return pjrpc.Response(
                    id=request.id,
                    result=http_response.json().get("result"),
                )

        yield send

@pytest.mark.order(1)
def test_write_ok(rpc_client):
    request = pjrpc.Request(
        id=1,
        method="write",
        params={
            "file_path": "test_file.txt",
            "content": "Hello, World!"
        }
    )
    response = rpc_client(request)
    assert response.id == 1
    assert "Successfully wrote" in response.result

@pytest.mark.order(2)
def test_read_ok(rpc_client):
    request = pjrpc.Request(
        id=1,
        method="read",
        params={
            "file_path": "test_file.txt",
            "max_length": 10
        }
    )
    response = rpc_client(request)
    assert response.id == 1
    assert response.result == "Hello, Wor"  # Assuming the content of test_file.txt is "Hello, World!"

@pytest.mark.order(3)
def test_shell_ok(rpc_client):
    request = pjrpc.Request(
        id=1,
        method="shell",
        params={
            "command": "chmod 400 test_file.txt"
        }
    )
    response = rpc_client(request)
    assert response.id == 1
    assert response.result == ""  # Assuming the command executes successfully

@pytest.mark.order(4)
def test_invalid_tool(rpc_client):
    request = pjrpc.Request(
        id=1,
        method="invalid_tool",
        params={}
    )
    response = rpc_client(request)
    assert response.id == 1
    assert response.error is not None
    assert response.error.code == -32600
    assert "Tool not found" in response.error.message

@pytest.mark.order(5)
def test_invalid_params(rpc_client):
    request = pjrpc.Request(
        id=1,
        method="write",
        params={"bad": "param"}  # This should be a dict, not a string
    )
    response = rpc_client(request)
    assert response.id == 1
    assert response.error is not None
    assert response.error.code == -32600
    assert "Bad request" in response.error.message

@pytest.mark.order(6)
def test_shell_timeout(rpc_client):
    request = pjrpc.Request(
        id=1,
        method="shell",
        params={
            "command": "yes",  # Infinite loop
            "timeout": 1  # Set a short timeout for testing
        }
    )
    response = rpc_client(request)
    assert response.id == 1
    assert "timed out" in response.result  # Assuming the command times out

def run():
    pytest.main(["-v", "src/mcp_serv/tests.py"])