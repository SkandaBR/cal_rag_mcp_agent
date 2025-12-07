from langchain.agents import initialize_agent, AgentType
from langchain.llms import Ollama
from langchain.tools import Tool
from mcp_client import client


# Wrap MCP tools for LangChain
retrieval_tool = Tool(
  name="MCP-RAG",
  func=lambda q: client.call_tool("rag_retrieve", {"query": q}),
  description="Retrieve info from RAG via MCP"
)


calc_tool = Tool(
  name="MCP-Calculator",
  func=lambda e: client.call_tool("calculator", {"expression": e}),
  description="Do arithmetic via MCP"
)


llm = Ollama(model="mistral")
agent = initialize_agent(
  tools=[retrieval_tool, calc_tool],
  llm=llm,
  agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
  verbose=True
)


query = "If Germany’s renewable energy sector was 250 TWh in 2023 and is projected to grow 10% per year, what will it reach by 2030, and how does this compare with Germany’s official renewable energy targets?"
print(agent.run(query))