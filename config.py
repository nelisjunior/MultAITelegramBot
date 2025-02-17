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
EDEN_AI_API_KEY = os.getenv('EDEN_AI_API_KEY')

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# API Configuration
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# Bot Messages
WELCOME_MESSAGE = """
👋 Welcome to AI Bot with Notion integration!

Available commands:
/start - Start the bot
/help - Show this help message
/save - Save message to Notion
/search - Search in Notion
/toggle_ai - Ativar/Desativar processamento de mensagens com IA
/use_deepseek - Alternar para DeepSeek AI
/use_eden - Alternar para Eden AI
/use_dummy - Ativar modo dummy (desativa todas as IAs)
/analyze_sentiment - Analisar sentimento da próxima mensagem

Just send me any message and I'll process it using AI!
"""

HELP_MESSAGE = """
🤖 AI Bot Help

Commands:
/start - Initialize the bot
/help - Show this help message
/save <title> - Save the next message to Notion with the given title
/search <query> - Search for pages in Notion
/toggle_ai - Ativar/Desativar processamento de mensagens com IA
/use_deepseek - Alternar para DeepSeek AI
/use_eden - Alternar para Eden AI
/use_dummy - Ativar modo dummy (desativa todas as IAs)
/analyze_sentiment - Analisar sentimento da próxima mensagem

Usage:
- Send any message to process it with AI (quando ativado)
- Use /save to store important messages in Notion
- Use /search to find stored information
- Use /toggle_ai para ativar/desativar a IA
- Use /use_deepseek ou /use_eden para escolher qual AI usar
- Use /use_dummy para desativar todas as IAs
- Use /analyze_sentiment antes de uma mensagem para análise de sentimento

Note: Please be patient as responses may take a few seconds to process.
"""

ERROR_MESSAGE = "Sorry, something went wrong. Please try again later."
PROCESSING_MESSAGE = "Processing your message... Please wait."