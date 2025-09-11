"""
Example tools for demonstrating Google Generative AI tool calling capabilities.
"""

from langchain_core.tools import tool
from datetime import datetime, timezone
import time


@tool(description="Get the current time in some timezone.")
def get_current_time(timezone_name: str = "UTC") -> str:
    """
    Get the current time in the specified timezone.
    
    Args:
        timezone_name: Timezone name (e.g., 'UTC', 'local')
    
    Returns:
        Current time formatted as a string
    """
    if timezone_name.upper() == "UTC":
        current_time = datetime.now(timezone.utc)
        return f"Current time in UTC: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    elif timezone_name.lower() == "local":
        current_time = datetime.now()
        return f"Current local time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
    else:
        # For simplicity, just return UTC time with a note
        current_time = datetime.now(timezone.utc)
        return f"Timezone '{timezone_name}' not supported. Current UTC time: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"


# List of all available tools
ALL_TOOLS = [
    get_current_time
]