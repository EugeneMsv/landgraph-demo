import os
from typing import List, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import BaseTool
from langchain_core.messages import ToolMessage
from state import State


class GeminiBot:
    """
    A Gemini-powered bot that accepts tools list and memory for LangGraph integration.
    """
    
    def __init__(self, tools: List[BaseTool] = None):
        """
        Initialize the Gemini bot with tools and memory.
        
        Args:
            tools: List of LangChain tools available to the bot
            memory: Memory component for the bot
        """
        self.tools = tools or []
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.1
        )
        
        # Bind tools to the LLM if tools are provided
        if self.tools:
            self.llm_with_tools = self.llm.bind_tools(self.tools)
        else:
            self.llm_with_tools = self.llm
    
    def process(self, state: State) -> State:
        """
        Process the current state and return updated state.
        
        Args:
            state: Current conversation state
            
        Returns:
            Updated state with bot response
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

