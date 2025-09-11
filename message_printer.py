from typing import List
from langchain_core.messages import BaseMessage


class MessagePrinter:
    """
    A utility class for printing conversation messages in a formatted way.
    """
    
    @staticmethod
    def print_conversation(messages: List[BaseMessage]) -> None:
        """
        Print a conversation from a list of messages.
        
        Args:
            messages: List of LangChain message objects
        """
        print("Conversation:")
        for message in messages:
            MessagePrinter._print_message(message)
    
    @staticmethod
    def _print_message(message: BaseMessage) -> None:
        """
        Print a single message with appropriate formatting.
        
        Args:
            message: A LangChain message object
        """
        if hasattr(message, 'type'):
            if message.type == "human":
                print(f"Human: {message.content}")
            elif message.type == "ai":
                # Handle AI messages with tool calls
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    print(f"Assistant: [Called tool: {message.tool_calls[0]['name']}]")
                else:
                    print(f"Assistant: {message.content}")
            elif message.type == "tool":
                print(f"Tool Result: {message.content}")
            else:
                print(f"Unknown message type: {message.type}")
        else:
            print(f"Message: {message}")