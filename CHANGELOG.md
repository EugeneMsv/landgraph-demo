# Changelog

All notable changes to this project will be documented in this file.

## [ada688a] - 2025-09-12

### Added
- Created modular architecture with AiBot abstract base class and GeminiBot implementation, enabling easy addition of new AI providers
- Organized code into packages: `bots/` for AI implementations and `tools/` for LangChain tools  
- Enhanced timezone support with pytz integration, allowing accurate time queries for any global timezone including DST handling