import asyncio
from typing import List, Any
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage, AIMessage
from mcp_use.client import MCPClient
from .ai_agent import AiAgent
from state import State


class ClaudeMcpAgent(AiAgent):
    """
    A Claude-powered agent that uses MCP protocol to connect to Claude Code server.
    This enables account-based authentication without requiring API keys.
    """

    def __init__(self, tools: List[BaseTool] = None):
        """
        Initialize the Claude MCP agent.

        Args:
            tools: List of LangChain tools available to the agent (ignored)
        """
        self.mcp_client = None
        # Skip the parent __init__ to avoid LLM initialization
        # Ignore tools parameter - we don't use them for MCP communication
        self._initialize_mcp_client()

    def _initialize_llm(self) -> Any:
        """
        Not used for MCP agent - we override process() directly.
        """
        return None

    def _initialize_mcp_client(self):
        """Initialize MCP client to connect to Claude Code server."""
        try:
            # Configure MCP client to connect to Claude Code server via STDIO
            config = {
                "mcpServers": {
                    "claude_code": {
                        "command": "claude",
                        "args": ["mcp", "serve"]
                    }
                }
            }

            self.mcp_client = MCPClient.from_dict(config)

        except Exception as e:
            print(f"Warning: Could not initialize MCP client: {e}")

    def process(self, state: State) -> State:
        """
        Process the current state using Claude via MCP.
        Overrides the parent method to use MCP instead of LLM.

        Args:
            state: Current conversation state

        Returns:
            Updated state with Claude's response
        """
        try:
            # Extract the latest human message
            human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]

            if human_messages:
                latest_query = human_messages[-1].content

                # Try to call Claude via MCP
                if self.mcp_client:
                    # Use asyncio to run the async MCP call
                    try:
                        response_content = asyncio.run(self._call_claude_mcp(latest_query))
                    except Exception as e:
                        response_content = f"Claude (via MCP): MCP call failed: {str(e)}"
                else:
                    response_content = f"Claude (via MCP): Could not initialize MCP client."
            else:
                response_content = "Claude (via MCP): Hello! Ready to process messages through MCP protocol."

            ai_msg = AIMessage(content=response_content)
            state["messages"].append(ai_msg)

        except Exception as e:
            error_msg = AIMessage(content=f"Claude MCP Error: {str(e)}")
            state["messages"].append(error_msg)

        return state

    async def _call_claude_mcp(self, query: str) -> str:
        """
        Call Claude through MCP protocol.
        Sends a query to Claude via the MCP client and returns the response.
        """
        if not self.mcp_client:
            raise RuntimeError("MCP client not initialized")

        try:
            # Create session with Claude Code server
            session = await self._create_session()

            # Execute the Task tool and get response
            response_text = await self._execute_task_tool(session, query)
            return f"Claude (via MCP): {response_text}"

        except Exception as e:
            return f"Claude (via MCP): Error - {str(e)}"

        finally:
            # Clean up sessions
            try:
                await self.mcp_client.close_all_sessions()
            except:
                pass

    async def _create_session(self):
        """
        Create and return the first available MCP session.

        Returns:
            The MCP session object for communication with Claude Code server

        Raises:
            RuntimeError: If no sessions are available after creation
        """
        await self.mcp_client.create_all_sessions()

        sessions = self.mcp_client.sessions
        if not sessions:
            raise RuntimeError("No MCP sessions available")

        session_name = list(sessions.keys())[0]
        return self.mcp_client.get_session(session_name)

    async def _execute_task_tool(self, session, query: str) -> str:
        """
        Execute the Task tool with the given query and return response text.

        Args:
            session: MCP session to use for tool execution
            query: User query to process

        Returns:
            Response text from the Task tool execution
        """
        # List available tools from Claude Code
        tools = await session.list_tools()

        # List all available tools first
        tool_names = [tool.name for tool in tools]
        print(tool_names)

        # Look for a 'Task' tool which seems to be the main agent interface
        task_tool = next((tool for tool in tools if tool.name == 'Task'), None)

        if task_tool:
            # Use the Task tool with general-purpose agent to handle our query
            result = await session.call_tool(
                name="Task",
                arguments={
                    "description": "Answer user question",
                    "prompt": query,
                    "subagent_type": "general-purpose"
                }
            )

            if result and hasattr(result, 'content') and result.content:
                content = result.content[0] if isinstance(result.content, list) else result.content
                response_text = content.text if hasattr(content, 'text') else str(content)
                return response_text
            else:
                return "Task tool executed but returned no content"
        else:
            # Just show available tools for debugging
            return f"Connected successfully! Available tools: {', '.join(tool_names)}"

    def cleanup(self):
        """Clean up MCP resources."""
        if self.mcp_client:
            # Note: cleanup would be async in real implementation
            # await self.mcp_client.close_all_sessions()
            pass