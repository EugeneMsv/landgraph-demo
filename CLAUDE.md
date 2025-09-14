# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangGraph demonstration project that integrates Google's Gemini AI with tool calling capabilities. The project demonstrates how to build a conversational AI agent using LangGraph's StateGraph architecture with Google Generative AI models and LangChain tool integration.

## Key Architecture Components

### Core Components
- **`AiAgent`** (`agents/ai_agent.py`): Abstract base class that defines the common interface for AI agents, containing the generic `process_message` method for single message processing and tool execution
- **`GeminiAgent`** (`agents/gemini_agent.py`): Concrete implementation that inherits from `AiAgent` and implements Gemini-specific LLM initialization using ChatGoogleGenerativeAI
- **`ClaudeMcpAgent`** (`agents/claude_mcp_agent.py`): MCP protocol implementation for connecting to Claude Code server with account-based authentication, overrides `process_message` for MCP communication
- **`State`** (`state.py`): TypedDict defining the workflow state structure with ask, analysis_output, critic_output fields and `StatePrinter` utility
- **`tools/`**: Package containing organized LangChain tools:
  - **`date_time_tool.py`**: Date and time utilities with full timezone support using pytz
  - **`__init__.py`**: Package initialization and tool aggregation
- **`agents/`**: Package containing AI agent implementations
- **`main.py`**: Entry point that demonstrates the LangGraph setup and conversation flow
- **`message_printer.py`**: Utility class for formatted printing of conversation messages with proper handling of different message types

### LangGraph Architecture
The project uses LangGraph's StateGraph pattern with a multi-node critique workflow:
1. **Gemini Analysis Node** (`gemini_analysis`): Processes user queries and generates analysis using GeminiAgent
2. **Claude Critique Node** (`claude_critic`): Reviews analysis using ClaudeMcpAgent and provides structured feedback
3. **Conditional Edges**: Routes flow based on critique severity - continues analysis if critical/major issues found
4. **Iterative Refinement**: Allows re-analysis with critique context for improved results
5. **State-based Communication**: Nodes communicate via shared State object with structured fields

### Tool Integration
Tools are implemented using LangChain's `@tool` decorator and bound to the LLM using the standard LangChain approach. The architecture handles:
- **`AiAgent`** base class: Contains generic tool execution logic in the `process_message` method
- **Tool binding**: LLM instances are bound to tools using `bind_tools()` method in the base class constructor
- **Tool execution**: Automatic tool call detection and execution via `tool_calls` attribute
- **Tool response integration**: Tool results are added as `ToolMessage` instances with proper `tool_call_id`
- **Message-based processing**: Single BaseMessage input/output for better modularity and testability

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

### Message Processing Flow
1. Single BaseMessage is processed via `process_message()` method in `AiAgent` implementations
2. Message triggers LLM response via `llm_with_tools.invoke()` with message array
3. If response contains `tool_calls`, each tool is executed by finding it in the tools list
4. Tool results are added as `ToolMessage` instances with proper `tool_call_id` to message array
5. Final LLM response is generated after all tool executions complete and returned as BaseMessage

### Architecture Benefits
The refactored architecture provides:
- **Modularity**: Message-based processing allows agents to be used independently or within complex workflows
- **Extensibility**: Easy to add new AI providers (OpenAI, Claude, etc.) by creating new classes that inherit from `AiAgent`
- **Code Reuse**: Common tool execution logic is shared across all AI provider implementations
- **Separation of Concerns**: Provider-specific initialization is separated from generic processing logic
- **Testability**: Single message input/output makes unit testing straightforward
- **Workflow Composition**: Agents can be easily integrated into LangGraph workflows with conditional routing

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
4. Tools are automatically bound to the agent instance via `bind_tools()` in the `AiAgent` constructor
5. No additional configuration needed - tools are discovered by name during execution

### Tool Organization
The tools are organized by category:
- **Date/Time Tools**: `tools/date_time_tool.py` - Contains timezone-aware time utilities
- **Future Tool Categories**: Can be added as separate files (e.g., `math_tools.py`, `web_tools.py`)
- **Aggregation**: `tools/__init__.py` combines all tool categories into `ALL_TOOLS`

### Adding New AI Providers
To add support for a new AI provider (e.g., OpenAI, Claude):
1. Create a new class that inherits from `AiAgent` (e.g., `OpenAIAgent`, `ClaudeAgent`)
2. Implement the abstract `_initialize_llm()` method with provider-specific configuration
3. Optionally override `process_message()` for custom processing (like `ClaudeMcpAgent` does for MCP)
4. The base `process_message()` method and tool handling is inherited automatically
5. Update workflow nodes in `main.py` to use the new agent implementation

### State Management
The `State` TypedDict contains structured fields for workflow coordination:
- **`ask`**: Original user question or input that drives the analysis
- **`node_instruction`**: Current instruction written by each node for processing context
- **`analysis_output`**: Gemini's analysis result from the analysis node
- **`critic_output`**: Claude's critique response with structured feedback (raw_response format)
- **`StatePrinter`**: Utility class for formatted state visualization across workflow steps

### Workflow Execution
The critique workflow follows this pattern:
1. **Initial Analysis**: Gemini processes the user's `ask` and generates `analysis_output`
2. **Critique Phase**: Claude reviews the analysis and provides `critic_output`
3. **Conditional Routing**: If critical/major issues found, route back to analysis with critique context
4. **Iterative Refinement**: Continue until satisfactory analysis achieved
5. **State Visualization**: `StatePrinter` provides formatted output at each step