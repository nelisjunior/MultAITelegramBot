import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

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
👋 Welcome to DeepSeek Bot!

Available commands:
/start - Start the bot
/help - Show this help message

Just send me any message and I'll process it using DeepSeek AI!
"""

HELP_MESSAGE = """
🤖 DeepSeek Bot Help

Commands:
/start - Initialize the bot
/help - Show this help message

Usage:
Simply send any message, and I'll process it using DeepSeek AI to provide you with a response.

Note: Please be patient as responses may take a few seconds to process.
"""

ERROR_MESSAGE = "Sorry, something went wrong. Please try again later."
PROCESSING_MESSAGE = "Processing your message... Please wait."
