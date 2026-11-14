from pjrpc.common.exceptions import JsonRpcError

class ToolNotFoundError(JsonRpcError):
    def __init__(self, tool_name: str):
        super().__init__(
            code=-32600,
            message=f"Tool not found: {tool_name}",
        )

class BadRequestError(JsonRpcError):
    def __init__(self):
        super().__init__(
            code=-32600,
            message="Bad request. Requests must be valid JSON-RPC 2.0 requests with a method and optional parameters.",
        )

class NonexistentFileError(JsonRpcError):
    def __init__(self, file_path: str):
        super().__init__(
            code=-32001,
            message=f"File not found: {file_path}",
        )

class PermissionDeniedError(JsonRpcError):
    def __init__(self):
        super().__init__(
            code=-32002,
            message="Permission denied",
        )

class UnknownError(JsonRpcError):
    def __init__(self):
        super().__init__(
            code=-32003,
            message="An unknown error occurred",
        )