from fastmcp import FastMCP
from utils.retrieval import hybrid_search
from utils.generation import generate_answer
import math


mcp = FastMCP("rag_mcp_server")


@mcp.tool()
def rag_retrieve(query: str) -> str:
  """Retrieve relevant context using hybrid RAG."""
  docs = hybrid_search(query, top_k=3)
  return "\n---\n".join(docs)


@mcp.tool()
def calculator(expression: str) -> str:
  """Safe calculator for arithmetic expressions."""
  try:
    return str(eval(expression, {"__builtins__": {}}, {"math": math}))
  except Exception as e:
    return f"CALC_ERROR: {e}"


if __name__ == "__main__":
  mcp.run()