# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangGraph demonstration project that integrates Google's Gemini AI with tool calling capabilities. The project demonstrates how to build a conversational AI agent using LangGraph's StateGraph architecture with Google Generative AI models and LangChain tool integration.

## Key Architecture Components

### Core Components
- **`AiBot`** (`bots/ai_bot.py`): Abstract base class that defines the common interface for AI bots, containing the generic `process` method for tool execution and state management
- **`GeminiBot`** (`bots/gemini_bot.py`): Concrete implementation that inherits from `AiBot` and implements Gemini-specific LLM initialization using ChatGoogleGenerativeAI
- **`State`** (`state.py`): TypedDict defining the conversation state structure with message history
- **`tools/`**: Package containing organized LangChain tools:
  - **`date_time_tool.py`**: Date and time utilities with full timezone support using pytz
  - **`__init__.py`**: Package initialization and tool aggregation
- **`bots/`**: Package containing AI bot implementations
- **`main.py`**: Entry point that demonstrates the LangGraph setup and conversation flow
- **`message_printer.py`**: Utility class for formatted printing of conversation messages with proper handling of different message types

### LangGraph Architecture
The project uses LangGraph's StateGraph pattern:
1. Single node (`gemini_analysis`) that processes messages through the GeminiBot
2. Simple stateless conversation flow without persistent memory
3. Direct message processing and tool execution within the graph node

### Tool Integration
Tools are implemented using LangChain's `@tool` decorator and bound to the LLM using the standard LangChain approach. The architecture handles:
- **`AiBot`** base class: Contains generic tool execution logic in the `process` method
- **Tool binding**: LLM instances are bound to tools using `bind_tools()` method in the base class constructor
- **Tool execution**: Automatic tool call detection and execution via `tool_calls` attribute
- **Tool response integration**: Tool results are added as `ToolMessage` instances with proper `tool_call_id`
- **Final response generation**: After tool execution, a final LLM response is generated

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
1. User message triggers LLM response via `llm_with_tools.invoke()` in the `AiBot.process()` method
2. If response contains `tool_calls`, each tool is executed by finding it in the tools list
3. Tool results are added as `ToolMessage` instances with proper `tool_call_id`
4. Final LLM response is generated after all tool executions complete
5. All messages (AI, Tool, Final AI) are appended to the conversation state

### Architecture Benefits
The refactored architecture provides:
- **Extensibility**: Easy to add new AI providers (OpenAI, Claude, etc.) by creating new classes that inherit from `AiBot`
- **Code Reuse**: Common tool execution logic is shared across all AI provider implementations
- **Separation of Concerns**: Provider-specific initialization is separated from generic processing logic
- **Maintainability**: Changes to tool handling only need to be made in one place (`AiBot`)

### Message Handling
The `MessagePrinter` class provides formatted output for different message types:
- Human messages: Display content directly
- AI messages with tool calls: Show tool call indication
- AI messages without tool calls: Display response content
- Tool messages: Show tool execution results

### Adding New Tools
1. Create tool functions using `@tool` decorator in appropriate tool files (e.g., `tools/date_time_tool.py`)
2. Add to the specific tool category list (e.g., `ALL_DATE_TIME_TOOLS`)
3. Update `tools/__init__.py` to include in `ALL_TOOLS` aggregation
4. Tools are automatically bound to the bot instance via `bind_tools()` in the `AiBot` constructor
5. No additional configuration needed - tools are discovered by name during execution

### Tool Organization
The tools are organized by category:
- **Date/Time Tools**: `tools/date_time_tool.py` - Contains timezone-aware time utilities
- **Future Tool Categories**: Can be added as separate files (e.g., `math_tools.py`, `web_tools.py`)
- **Aggregation**: `tools/__init__.py` combines all tool categories into `ALL_TOOLS`

### Adding New AI Providers
To add support for a new AI provider (e.g., OpenAI, Claude):
1. Create a new class that inherits from `AiBot` (e.g., `OpenAIBot`, `ClaudeBot`)
2. Implement the abstract `_initialize_llm()` method with provider-specific configuration
3. The `process()` method and tool handling is inherited automatically
4. Update `main.py` to use the new bot implementation

### State Management
The `State` TypedDict contains a `messages` list that accumulates the entire conversation history including:
- Human messages (user input)
- AI messages (LLM responses, may include tool calls)
- Tool messages (tool execution results)
- Final AI messages (responses after tool execution)
- Whenever you're asked to make a git commit you must update CLAUDE.md and CHANGELOG.MD
- The CHANGELOG.MD is updated only in an append only mode, every new changes must have a commit hash of the change and a higlevel changes decsription ideally not more then 3 sentences and some business level