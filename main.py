from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import HumanMessage
from state import State
from gemini_bot import GeminiBot
from example_tools import ALL_TOOLS
from message_printer import MessagePrinter

load_dotenv()

# Initialize Gemini bot instance with tools and memory
gemini_bot = GeminiBot(tools=ALL_TOOLS)

def gemini_node(state: State) -> State:
    return gemini_bot.process(state)

def main():
    print("LangGraph Demo - Creating a simple graph with Gemini LLM")
    
    # Create a StateGraph
    graph = StateGraph(State)
    graph.add_edge(START, "gemini_analysis")
    graph.add_node("gemini_analysis", gemini_node)
    graph.add_edge("gemini_analysis", END)
    app = graph.compile()

    print("===START Interaction ===")
    result = app.invoke({
        "messages": [HumanMessage(content="Hello! What's the current time in "
                                          "UTC and in Seattle?")]
    })
    
    MessagePrinter.print_conversation(result["messages"])

    print("===END Interaction ===")

if __name__ == "__main__":
    main()
