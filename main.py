from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import HumanMessage
from state import State, StatePrinter
from agents import GeminiAgent, ClaudeMcpAgent
from tools import ALL_TOOLS
from message_printer import MessagePrinter

load_dotenv()

# Initialize Gemini bot instance with tools and memory
gemini_agent = GeminiAgent(tools=ALL_TOOLS)
claude_agent = ClaudeMcpAgent(tools=ALL_TOOLS)

def gemini_agent_node(state: State) -> State:
    # Check if this is a loop-back (critique exists)
    if state.get("critic_output"):
        # Re-analysis with critique context
        critique = state["critic_output"]["raw_response"]
        instruction = f"Re-analyze this query addressing the following critique:\n\nOriginal Query: {state['ask']}\n\nCritique to address: {critique}\n\nProvide improved analysis."
    else:
        # First analysis
        instruction = f"Analyze: {state['ask']}"

    # Store instruction in state
    state["node_instruction"] = instruction

    # Create message for AI agent and get response
    agent_message = HumanMessage(content=instruction)
    response_message = gemini_agent.process_message(agent_message)

    # Extract analysis output from response
    state["analysis_output"] = response_message.content
    StatePrinter.print_state(state)
    return state

def claude_agent_node(state: State) -> State:
    # Create instruction for Claude
    instruction = f"Critique this analysis and return JSON with critical, major, minor issues: {state['analysis_output']}"

    # Store instruction in state
    state["node_instruction"] = instruction

    # Create message for AI agent and get response
    agent_message = HumanMessage(content=instruction)
    response_message = claude_agent.process_message(agent_message)

    # For now, store the raw response - we'll add parsing later
    state["critic_output"] = {"raw_response": response_message.content}
    StatePrinter.print_state(state)
    return state

def should_continue_analysis(state: State) -> str:
    """Determine if analysis should continue based on critique."""
    # For now, just check if critic_output exists and has content
    # Later we'll parse JSON and check for critical/major issues
    critic_output = state.get("critic_output", {})
    raw_response = critic_output.get("raw_response", "")

    # Simple check - if critique mentions "critical" or "major" issues, continue
    if "critical" in raw_response.lower() or "major" in raw_response.lower():
        print("Found critical or major issues, continuing analysis...")
        return "gemini_analysis"
    else:
        print("No critical or major issues found, finishing...")
        return "END"

def main():
    print("LangGraph Demo")
    
    # Create a StateGraph
    graph = StateGraph(State)
    graph.add_edge(START, "gemini_analysis")
    graph.add_node("gemini_analysis", gemini_agent_node)
    graph.add_node("claude_critic", claude_agent_node)
    graph.add_edge("gemini_analysis", "claude_critic")
    graph.add_conditional_edges(
        "claude_critic",
        should_continue_analysis,
        {
            "gemini_analysis": "gemini_analysis",
            "END": END
        }
    )
    app = graph.compile()

    print("===START Interaction ===")

    # Create initial state dictionary
    initial_state = {
        "ask": "Are social networks good? Let's try to understand the benefits.",
        "node_instruction": None,
        "analysis_output": None,
        "critic_output": None
    }

    result = app.invoke(initial_state)

    print(f"\n🎉 WORKFLOW COMPLETED! 🎉")
    StatePrinter.print_state(result)

    print("===END Interaction ===")

if __name__ == "__main__":
    main()
