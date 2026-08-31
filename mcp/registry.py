from typing import Dict, Callable, Any, List
from mcp.protocol import ToolDefinition

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._defs: Dict[str, ToolDefinition] = {}

    def register(self, name: str, description: str, input_schema: dict, handler: Callable):
        self._tools[name] = handler
        self._defs[name] = ToolDefinition(name=name, description=description, inputSchema=input_schema)

    def get(self, name: str) -> Callable:
        return self._tools.get(name)

    def list_tools(self) -> List[ToolDefinition]:
        return list(self._defs.values())

    def call(self, name: str, arguments: dict) -> Any:
        handler = self.get(name)
        if not handler:
            raise ValueError(f"Tool not found: {name}")
        return handler(**arguments)

registry = ToolRegistry()
