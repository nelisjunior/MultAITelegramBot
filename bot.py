import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from config import TELEGRAM_TOKEN, WELCOME_MESSAGE, HELP_MESSAGE, ERROR_MESSAGE
from deepseek_client import DeepSeekClient
from notion_manager import NotionManager

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize clients
deepseek_client = DeepSeekClient()
notion_client = NotionManager()

# Cache for Notion context
notion_context = {}

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(WELCOME_MESSAGE)

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(HELP_MESSAGE)

async def list_databases(update: Update, context: CallbackContext) -> None:
    """List all accessible Notion databases."""
    try:
        databases = await notion_client.list_databases()
        if not databases:
            await update.message.reply_text("No databases found in your Notion workspace.")
            return

        response = "📚 Available Notion Databases:\n\n"
        for db in databases:
            response += f"📁 {db['title']}\n"
            response += f"ID: {db['id']}\n\n"

        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error listing databases: {str(e)}")
        await update.message.reply_text(ERROR_MESSAGE)

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle all incoming messages with AI assistance."""
    try:
        user_id = update.effective_user.id

        # Get current Notion context for the user
        if user_id not in notion_context:
            try:
                databases = await notion_client.list_databases()
                notion_context[user_id] = {
                    "databases": databases
                }
            except Exception as e:
                logger.warning(f"Could not fetch Notion context: {str(e)}")
                notion_context[user_id] = {}

        # Get AI response with Notion context
        response = await deepseek_client.get_response(
            update.message.text,
            context=notion_context.get(user_id, {})
        )

        # Process AI response and execute Notion actions if needed
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
        application.add_handler(CommandHandler("databases", list_databases))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Start the Bot
        logger.info("Starting bot...")
        application.run_polling()

    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        raise

if __name__ == '__main__':
    main()