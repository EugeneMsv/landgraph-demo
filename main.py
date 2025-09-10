from langgraph.graph import StateGraph, END, START
from langchain_core.messages import HumanMessage
from typing import TypedDict, List, Literal

class State(TypedDict):
    amount_gbp: float
    target_currency: Literal["USD", "EUR"]
    converted_amount: float

def convert_to_usd(state: State) -> State:
  state["converted_amount"] = state["amount_gbp"] * 1.35
  return state

def convert_to_eur(state: State) -> State:
  state["converted_amount"] = state["amount_gbp"] * 1.16
  return state

def choose_conversion(state: State) -> str:
  return state["target_currency"]

def main():
    print("LangGraph Demo - Creating a simple graph")
    
    # Create a StateGraph
    graph = StateGraph(State)
    graph.add_conditional_edges(START, choose_conversion, {
        "USD": "convert_to_usd",
        "EUR": "convert_to_eur"
    })

    graph.add_node("convert_to_usd", convert_to_usd)
    graph.add_node("convert_to_eur", convert_to_eur)


    graph.add_edge(["convert_to_usd", "convert_to_eur"], END)

    # Compile the graph
    app = graph.compile()
    
    # Test the graph
    result = app.invoke({"amount_gbp": 100, "target_currency": "EUR"})
    print(f"Graph result: {result}")
    print("LangGraph is working correctly!")

if __name__ == "__main__":
    main()
