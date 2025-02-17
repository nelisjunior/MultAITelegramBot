import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update
import logging

from config import TELEGRAM_TOKEN, WELCOME_MESSAGE, HELP_MESSAGE, PROCESSING_MESSAGE, ERROR_MESSAGE
from deepseek_client import DeepSeekClient
from utils import error_handler, send_typing_action

# Configure logging
logger = logging.getLogger(__name__)

# Initialize DeepSeek client
deepseek_client = DeepSeekClient()

@error_handler
async def start_command(update: Update, context: CallbackContext) -> None:
    """Handle the /start command"""
    await update.message.reply_text(WELCOME_MESSAGE)

@error_handler
async def help_command(update: Update, context: CallbackContext) -> None:
    """Handle the /help command"""
    await update.message.reply_text(HELP_MESSAGE)

@error_handler
async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages"""
    if not update.message or not update.message.text:
        await update.message.reply_text("Please send a text message.")
        return

    # Send "typing" action
    await send_typing_action(update, context)

    # Send processing message
    processing_message = await update.message.reply_text(PROCESSING_MESSAGE)

    try:
        # Get response from DeepSeek
        response = await deepseek_client.get_response(update.message.text)

        # Delete processing message
        await processing_message.delete()

        # Send response
        await update.message.reply_text(response)

    except TimeoutError:
        await processing_message.edit_text("Request timed out. Please try again.")
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        await processing_message.edit_text(ERROR_MESSAGE)

async def main() -> None:
    """Start the bot"""
    try:
        # Create application
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Start the bot
        logger.info("Starting bot...")
        await application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())