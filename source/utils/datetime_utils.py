from datetime import datetime

import pytz

from source.utils.logging_config import logger


async def get_current_datetime(timezone_name: str) -> str:
    """Return the current time in the configured timezone."""
    try:
        timezone = pytz.timezone(timezone_name)
        return datetime.now(timezone).isoformat()
    except Exception as error:
        logger.error(f"Error getting current datetime: {error}")
        return datetime.now(pytz.UTC).isoformat()