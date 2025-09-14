from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import HumanMessage
from state import State
from agents import GeminiAgent, ClaudeMcpAgent
from tools import ALL_TOOLS
from message_printer import MessagePrinter

load_dotenv()

# Initialize Gemini bot instance with tools and memory
gemini_agent = GeminiAgent(tools=ALL_TOOLS)
claude_agent = ClaudeMcpAgent(tools=ALL_TOOLS)

def gemini_agent_node(state: State) -> State:
    return gemini_agent.process(state)

def claude_agent_node(state: State) -> State:
    return claude_agent.process(state)

def main():
    print("LangGraph Demo - Creating a simple graph with Gemini LLM")
    
    # Create a StateGraph
    graph = StateGraph(State)
    graph.add_edge(START, "gemini_analysis")
    graph.add_node("gemini_analysis", gemini_agent_node)
    # graph.add_node("claude_critic", claude_agent_node)
    graph.add_edge("gemini_analysis", END)
    app = graph.compile()

    print("===START Interaction ===")
    result = app.invoke({
        "messages": [HumanMessage(content="Hello! What are you? What's the current time in "
                                          "UTC and in Seattle? Also please calculate time zone shift.")]
    })
    
    MessagePrinter.print_conversation(result["messages"])

    print("===END Interaction ===")

if __name__ == "__main__":
    main()
