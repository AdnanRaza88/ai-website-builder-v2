from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[str | int] = None
    method: str
    params: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[str | int] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None

class MCPNotification(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Dict[str, Any]] = None

class ToolDefinition(BaseModel):
    name: str
    description: str
    inputSchema: Dict[str, Any]

class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]
