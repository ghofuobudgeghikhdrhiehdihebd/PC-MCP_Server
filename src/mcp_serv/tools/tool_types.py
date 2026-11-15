from typing import Any, Literal
from dataclasses import dataclass

@dataclass
class ToolRequest:
    tool: str
    params: dict[str, Any]

@dataclass
class ToolResultSuccess:
    status: Literal["success"]
    result: str

@dataclass
class ToolResultError:
    status: Literal["error"]
    error: str