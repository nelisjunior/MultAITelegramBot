import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# DeepSeek API Configuration
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Bot Messages
WELCOME_MESSAGE = """
👋 Welcome to DeepSeek Bot with Notion integration!

Available commands:
/start - Start the bot
/help - Show this help message
/save - Save message to Notion
/search - Search in Notion

Just send me any message and I'll process it using DeepSeek AI!
"""

HELP_MESSAGE = """
🤖 DeepSeek Bot Help

Commands:
/start - Initialize the bot
/help - Show this help message
/save <title> - Save the next message to Notion with the given title
/search <query> - Search for pages in Notion

Usage:
- Send any message to process it with DeepSeek AI
- Use /save to store important messages in Notion
- Use /search to find stored information

Note: Please be patient as responses may take a few seconds to process.
"""

ERROR_MESSAGE = "Sorry, something went wrong. Please try again later."
PROCESSING_MESSAGE = "Processing your message... Please wait."