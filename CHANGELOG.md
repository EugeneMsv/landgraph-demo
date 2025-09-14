# Changelog

All notable changes to this project will be documented in this file.

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