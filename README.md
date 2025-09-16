# LangGraph Multi-Agent AI Demo

**Executive Summary:** This demonstration showcases enterprise-ready AI workflow automation where multiple AI agents collaborate, critique each other's work, and iteratively improve results - proving how AI systems can achieve higher quality outputs through automated peer review.

## What This Demonstrates

 **Multi-Agent AI Collaboration** - Gemini and Claude AI work together in a structured workflow
 **Automated Quality Assurance** - AI agents critique and improve each other's analysis
 **Iterative Improvement** - System automatically refines outputs until quality standards are met
 **Enterprise Workflow Orchestration** - Configurable, scalable workflow management

## Quick Demo

### Prerequisites
- Python 3.11+
- Gemini API key
- **Claude Code** installed (connects via MCP for agent communication)

### Run the Demo
```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Set up environment
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 3. Install dependencies
pip install -e .

# 4. Run the demonstration
python main.py
```

## What You'll See

The demo analyzes the question *"Are social networks good?"* through a collaborative AI workflow:

1. **Gemini** performs initial analysis
2. **Claude** critiques the analysis for quality issues
3. **System** automatically routes back for improvement if critical issues found
4. **Result** delivers a thoroughly reviewed, high-quality analysis

## Business Applications

- **Research & Analysis**: Automated peer review for reports and recommendations
- **Content Quality**: Multi-agent validation for customer-facing content
- **Decision Support**: Iterative analysis refinement for strategic decisions