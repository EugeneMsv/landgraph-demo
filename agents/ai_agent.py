from abc import ABC, abstractmethod
from typing import List, Any
from langchain_core.tools import BaseTool
from langchain_core.messages import ToolMessage
from state import State


class AiAgent(ABC):
    """
    Abstract base class for AI agents that can process messages and use tools.
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
    
    @abstractmethod
    def _initialize_llm(self) -> Any:
        """
        Initialize the specific LLM implementation.
        
        Returns:
            The initialized LLM instance
        """
        pass
    
    def process(self, state: State) -> State:
        """
        Process the current state and return updated state.
        
        Args:
            state: Current conversation state
            
        Returns:
            Updated state with agent response
        """
        # Get AI response (may contain tool calls)
        ai_msg = self.llm_with_tools.invoke(state["messages"])
        state["messages"].append(ai_msg)
        
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
                    state["messages"].append(tool_message)
            
            # Get final response after tool execution
            final_response = self.llm_with_tools.invoke(state["messages"])
            state["messages"].append(final_response)
        
        return state