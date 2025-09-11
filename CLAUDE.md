# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangGraph demonstration project that integrates Google's Gemini AI with tool calling capabilities. The project demonstrates how to build a conversational AI agent using LangGraph's StateGraph architecture with Google Generative AI models and LangChain tool integration.

## Key Architecture Components

### Core Components
- **`GeminiBot`** (`gemini_bot.py`): Main bot class that wraps ChatGoogleGenerativeAI with tool calling capabilities using proper LangChain tool binding
- **`State`** (`state.py`): TypedDict defining the conversation state structure with message history
- **`example_tools.py`**: Collection of LangChain tools that the bot can invoke (currently includes time utilities)
- **`main.py`**: Entry point that demonstrates the LangGraph setup and conversation flow
- **`message_printer.py`**: Utility class for formatted printing of conversation messages with proper handling of different message types

### LangGraph Architecture
The project uses LangGraph's StateGraph pattern:
1. Single node (`gemini_analysis`) that processes messages through the GeminiBot
2. Simple stateless conversation flow without persistent memory
3. Direct message processing and tool execution within the graph node

### Tool Integration
Tools are implemented using LangChain's `@tool` decorator and bound to the Gemini model using the standard LangChain approach. The `GeminiBot` class handles:
- Tool binding to the LLM instance using `bind_tools()` method
- Automatic tool call detection and execution via `tool_calls` attribute
- Tool response integration as `ToolMessage` instances
- Final response generation after tool execution

## Development Commands

### Running the Application
```bash
source .venv/bin/activate
python main.py
```

### Environment Setup
- Requires Python 3.11+
- Dependencies managed through `pyproject.toml`
- Needs `GEMINI_API_KEY` environment variable set (typically in `.env` file)
- Uses `gemini-2.5-flash` model

## Key Implementation Details

### Tool Execution Flow
1. User message triggers LLM response via `llm_with_tools.invoke()`
2. If response contains `tool_calls`, each tool is executed by finding it in the tools list
3. Tool results are added as `ToolMessage` instances with proper `tool_call_id`
4. Final LLM response is generated after all tool executions complete
5. All messages (AI, Tool, Final AI) are appended to the conversation state

### Message Handling
The `MessagePrinter` class provides formatted output for different message types:
- Human messages: Display content directly
- AI messages with tool calls: Show tool call indication
- AI messages without tool calls: Display response content
- Tool messages: Show tool execution results

### Adding New Tools
1. Create tool functions using `@tool` decorator in `example_tools.py`
2. Add to `ALL_TOOLS` list
3. Tools are automatically bound to the bot instance via `bind_tools()`
4. No additional configuration needed - tools are discovered by name during execution

### State Management
The `State` TypedDict contains a `messages` list that accumulates the entire conversation history including:
- Human messages (user input)
- AI messages (LLM responses, may include tool calls)
- Tool messages (tool execution results)
- Final AI messages (responses after tool execution)