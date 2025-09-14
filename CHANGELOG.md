# Changelog

All notable changes to this project will be documented in this file.

## [dc4239d] - 2025-09-14

### Added
- **Iteration Limiting**: Implemented configurable maximum iterations (default: 3) to prevent infinite critique loops
- **Immutable Configuration**: Added `Configuration` dataclass with `@dataclass(frozen=True)` for workflow settings
- **Iteration Tracking**: Added `current_iterations` counter in state management with progress visualization (X/Y format)
- **JSON Response Parsing**: Enhanced `ClaudeMcpAgent` with `_extract_readable_content()` method to parse Claude's JSON responses

### Changed
- **Enhanced State Management**: Updated `State` TypedDict to include `configuration` and `current_iterations` fields
- **Improved Workflow Control**: Modified `should_continue_analysis()` to check both critique severity AND iteration limits
- **Better User Experience**: `StatePrinter` now displays iteration progress and Claude responses are clean/readable instead of raw JSON
- **Graceful Error Handling**: Added fallback to original response if JSON parsing fails in Claude MCP agent

### Fixed
- **Infinite Loop Prevention**: Workflow now automatically terminates after maximum iterations even if issues persist
- **Clean Output**: Users no longer see raw JSON metadata from Claude responses, only readable content

## [2e09f57] - 2025-09-14

### Changed
- Refactored AI agents from State-based to message-based processing architecture for improved modularity and testability
- Implemented multi-node critique workflow with Gemini analysis and Claude critique phases, enabling iterative refinement based on feedback severity
- Redesigned State structure with dedicated fields (ask, analysis_output, critic_output) and added StatePrinter utility for workflow visualization

## [4f3ab20] - 2025-09-14

### Changed
- Refactored `bots/` package to `agents/` for better semantic clarity and consistency with AI agent terminology
- Renamed `AiBot` class to `AiAgent` to align with modern AI development conventions
- Added `ClaudeMcpAgent` implementation with MCP protocol integration for Claude Code server connectivity

## [ada688a] - 2025-09-12

### Added
- Created modular architecture with AiBot abstract base class and GeminiBot implementation, enabling easy addition of new AI providers
- Organized code into packages: `bots/` for AI implementations and `tools/` for LangChain tools
- Enhanced timezone support with pytz integration, allowing accurate time queries for any global timezone including DST handling