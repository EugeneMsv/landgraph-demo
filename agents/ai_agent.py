from abc import ABC, abstractmethod
from typing import List, Any
import time
from langchain_core.tools import BaseTool
from langchain_core.messages import BaseMessage, ToolMessage


class AiAgent(ABC):
    """
    Abstract base class for AI agents that process single BaseMessage input/output.
    Completely decoupled from State - works only with LangChain messages.
    """

    def __init__(self, tools: List[BaseTool] = None):
        """
        Initialize the AI agent with tools.

        Args:
            tools: List of LangChain tools available to the bot
        """
        self.tools = tools or []
        self.llm = self._initialize_llm()

        # Bind tools to the LLM if tools are provided
        if self.tools:
            self.llm_with_tools = self.llm.bind_tools(self.tools)
        else:
            self.llm_with_tools = self.llm

    def _process_message_internal(self, message: BaseMessage) -> BaseMessage:
        """
        Default internal message processing logic for LLM-based agents.
        Can be overridden by subclasses for custom processing.

        Args:
            message: Single LangChain BaseMessage

        Returns:
            Single BaseMessage response from the agent
        """
        # Create message list for LLM processing
        messages = [message]

        # Get AI response (may contain tool calls)
        ai_msg = self.llm_with_tools.invoke(messages)

        # If there are tool calls, execute them and get final response
        if hasattr(ai_msg, 'tool_calls') and ai_msg.tool_calls:
            # Execute each tool call
            for tool_call in ai_msg.tool_calls:
                # Find the tool by name
                tool = next((t for t in self.tools if t.name == tool_call["name"]), None)
                if tool:
                    # Execute the tool
                    tool_result = tool.invoke(tool_call["args"])
                    # Create tool message
                    tool_message = ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_call["id"]
                    )
                    messages.append(tool_message)

            # Get final response after tool execution
            ai_msg = self.llm_with_tools.invoke(messages)

        return ai_msg

    @abstractmethod
    def _initialize_llm(self) -> Any:
        """
        Initialize the specific LLM implementation.

        Returns:
            The initialized LLM instance
        """
        pass

    def process_message(self, message: BaseMessage) -> BaseMessage:
        """
        Process a single message and return the agent's response with timing measurement.

        Args:
            message: Single LangChain BaseMessage

        Returns:
            Single BaseMessage response from the agent
        """
        start_time = time.perf_counter()
        result = self._process_message_internal(message)
        end_time = time.perf_counter()
        print(f"⏱️  {self.__class__.__name__} processing time: {end_time - start_time:.2f}s")
        return result

