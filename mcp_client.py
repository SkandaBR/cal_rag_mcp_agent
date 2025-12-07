from mcp.client import MCPClient


client = MCPClient("http://localhost:8000") # server address


# Example: call RAG tool
print(client.call_tool("rag_retrieve", {"query": "Germany renewable policies"}))


# Example: call calculator tool
print(client.call_tool("calculator", {"expression": "25*4+10"}))
