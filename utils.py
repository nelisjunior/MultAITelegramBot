import logging
from functools import wraps
from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ChatAction

logger = logging.getLogger(__name__)

def error_handler(func):
    """
    Decorator for handling errors in bot commands and message handlers
    """
    @wraps(func)
    async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        try:
            return await func(update, context, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            if update.effective_message:
                await update.effective_message.reply_text(
                    "Sorry, an error occurred while processing your request. Please try again later."
                )
    return wrapper

async def send_typing_action(update: Update, context: CallbackContext):
    """
    Send typing action while processing message
    """
    await context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id,
        action=ChatAction.TYPING
    )