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
👋 Bem-vindo ao Bot com integração Notion e IAs!

Comandos disponíveis:
/start - Iniciar o bot
/help - Mostrar esta mensagem de ajuda
/save <título> - Salvar mensagem no Notion
/search <termo> - Buscar no Notion
/databases - Listar bancos de dados do Notion
/toggle_ai - Ativar/Desativar processamento de mensagens com IA
/use_deepseek - Alternar para DeepSeek AI
/use_eden - Alternar para Eden AI
/use_dummy - Ativar modo dummy (desativa todas as IAs)
/analyze_sentiment - Analisar sentimento da próxima mensagem

Envie qualquer mensagem para interagir com a IA ativa!
"""

HELP_MESSAGE = """
🤖 Ajuda do Bot

Comandos:
/start - Inicializar o bot
/help - Mostrar esta mensagem de ajuda
/save <título> - Salvar a próxima mensagem no Notion
/search <termo> - Buscar por páginas no Notion
/databases - Listar bancos de dados disponíveis no Notion
/toggle_ai - Ativar/Desativar processamento de mensagens com IA
/use_deepseek - Alternar para DeepSeek AI
/use_eden - Alternar para Eden AI
/use_dummy - Ativar modo dummy (desativa todas as IAs)
/analyze_sentiment - Analisar sentimento da próxima mensagem

Como usar:
- Use /save para armazenar mensagens importantes no Notion
- Use /search para encontrar informações salvas
- Use /databases para ver os bancos de dados disponíveis
- Envie mensagens normalmente para interagir com a IA (quando ativada)
- Use /toggle_ai para ativar/desativar a IA
- Use /use_deepseek ou /use_eden para escolher qual IA usar
- Use /use_dummy para desativar todas as IAs
- Use /analyze_sentiment antes de uma mensagem para análise de sentimento

Observação: As respostas podem levar alguns segundos para serem processadas.
"""

ERROR_MESSAGE = "Desculpe, ocorreu um erro. Por favor, tente novamente mais tarde."

PROCESSING_MESSAGE = "Processing your message... Please wait."