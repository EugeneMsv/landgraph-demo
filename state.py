from typing import TypedDict, Optional, Dict
from dataclasses import dataclass

@dataclass(frozen=True)
class Configuration:
    """Immutable configuration settings for the workflow."""
    max_iterations: int = 3

class State(TypedDict):
    ask: Optional[str]                    # User's original input/question
    node_instruction: Optional[str]       # Current instruction written by each node
    analysis_output: Optional[str]        # Gemini's analysis result
    critic_output: Optional[Dict]         # Claude's critique: {"critical": [], "major": [], "minor": []}
    configuration: Configuration          # Immutable configuration settings
    current_iterations: int               # Current iteration count

class StatePrinter:
    """Utility class for pretty printing state."""

    @staticmethod
    def print_state(state: State):
        """Pretty print the current state."""
        print(f"\n{'='*60}")
        print(f"📊 State:")
        print(f"{'='*60}")

        # Show iteration progress
        current_iter = state.get('current_iterations', 0)
        config = state.get('configuration')
        max_iter = config.max_iterations if config else 3
        print(f"🔄 Iteration: {current_iter}/{max_iter}")

        print(f"\n❓ ASK: {state.get('ask', 'None')}")

        print(f"\n🎯 NODE INSTRUCTION:")
        instruction = state.get('node_instruction', 'None')
        print(f"   {instruction}")

        print(f"\n🤖 ANALYSIS OUTPUT:")
        analysis = state.get('analysis_output', 'None')
        print(f"   {analysis}")

        print(f"\n🔍 CRITIC OUTPUT:")
        critic = state.get('critic_output', {})
        if critic:
            if isinstance(critic, dict):
                for key, value in critic.items():
                    print(f"   {key}: {value}")
            else:
                print(f"   {critic}")
        else:
            print("   None")

        print(f"{'='*60}\n")