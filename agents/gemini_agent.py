import os
from typing import List, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import BaseTool
from .ai_agent import AiAgent


class GeminiAgent(AiAgent):
    """
    A Gemini-powered bot that accepts tools list and memory for LangGraph integration.
    """
    
    def __init__(self, tools: List[BaseTool] = None):
        """
        Initialize the Gemini bot with tools.
        
        Args:
            tools: List of LangChain tools available to the bot
        """
        super().__init__(tools)
    
    def _initialize_llm(self) -> ChatGoogleGenerativeAI:
        """
        Initialize the Gemini LLM with specific configuration.
        
        Returns:
            The initialized ChatGoogleGenerativeAI instance
        """
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.1
        )
    

