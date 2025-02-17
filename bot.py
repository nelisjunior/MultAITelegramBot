import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from config import TELEGRAM_TOKEN, WELCOME_MESSAGE, HELP_MESSAGE, ERROR_MESSAGE
from deepseek_client import DeepSeekClient

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize DeepSeek client
deepseek_client = DeepSeekClient()

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(WELCOME_MESSAGE)

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(HELP_MESSAGE)

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle all incoming messages."""
    try:
        # Get response from DeepSeek
        response = await deepseek_client.get_response(update.message.text)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

def main() -> None:
    """Start the bot."""
    try:
        # Create the Application
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Start the Bot
        logger.info("Starting bot...")
        application.run_polling()

    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        raise

if __name__ == '__main__':
    main()