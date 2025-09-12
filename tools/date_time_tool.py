"""
Date and time tools for getting current time in any timezone.
"""

from langchain_core.tools import tool
from datetime import datetime, timezone
import pytz


@tool(description="Get the current time in any timezone.")
def get_current_time(timezone_name: str = "UTC") -> str:
    """
    Get the current time in the specified timezone.
    
    Args:
        timezone_name: Timezone name (e.g., 'UTC', 'US/Eastern', 'Europe/London', 'America/Los_Angeles')
    
    Returns:
        Current time formatted as a string
    """
    try:
        if timezone_name.upper() == "UTC":
            current_time = datetime.now(timezone.utc)
            return f"Current time in UTC: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        elif timezone_name.lower() == "local":
            current_time = datetime.now()
            return f"Current local time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            # Use pytz to support any timezone
            tz = pytz.timezone(timezone_name)
            current_time = datetime.now(tz)
            return f"Current time in {timezone_name}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except pytz.exceptions.UnknownTimeZoneError:
        # If timezone is not recognized, return UTC with error message
        current_time = datetime.now(timezone.utc)
        return f"Unknown timezone '{timezone_name}'. Available timezones include: US/Eastern, US/Pacific, Europe/London, Europe/Paris, Asia/Tokyo, Australia/Sydney, etc. Current UTC time: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except Exception as e:
        # Handle any other errors
        current_time = datetime.now(timezone.utc)
        return f"Error getting time for timezone '{timezone_name}': {str(e)}. Current UTC time: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"


# List of all available date/time tools
ALL_DATE_TIME_TOOLS = [
    get_current_time
]