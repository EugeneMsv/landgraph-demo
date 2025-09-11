from langchain_core.messages import HumanMessage
from typing import TypedDict, List

class State(TypedDict):
  messages: List[HumanMessage]