import logging
from functools import wraps

logger = logging.getLogger(__name__)

def error_handler(func):
    """
    Decorator for handling errors in bot commands and message handlers
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            if args and hasattr(args[0], 'message'):
                await args[0].message.reply_text(
                    "Sorry, an error occurred while processing your request. Please try again later."
                )
    return wrapper