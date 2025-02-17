import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from config import TELEGRAM_TOKEN, WELCOME_MESSAGE, HELP_MESSAGE, ERROR_MESSAGE
from deepseek_client import DeepSeekClient
from eden_client import EdenAIClient
from notion_manager import NotionManager
from ai_manager import AIManager, AIProvider

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize clients and managers
deepseek_client = DeepSeekClient()
eden_client = EdenAIClient()
notion_client = NotionManager()
ai_manager = AIManager()

# Cache for context
notion_context = {}
analyzing_sentiment = {}  # Dicionário para controlar análise de sentimento

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    ai_manager.initialize_user(user_id)  # Inicializa com configurações padrão
    await update.message.reply_text(WELCOME_MESSAGE)

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(HELP_MESSAGE)

async def toggle_ai(update: Update, context: CallbackContext) -> None:
    """Toggle AI processing for the user."""
    user_id = update.effective_user.id
    if ai_manager.is_enabled(user_id):
        ai_manager.disable_ai(user_id)
        await update.message.reply_text("🔇 IA está agora desativada. Suas mensagens não serão processadas.")
    else:
        provider = ai_manager.enable_ai(user_id)
        provider_name = AIManager.get_provider_name(provider)
        await update.message.reply_text(f"🤖 IA está agora ativada usando {provider_name}!")

async def use_deepseek(update: Update, context: CallbackContext) -> None:
    """Switch to DeepSeek AI."""
    user_id = update.effective_user.id
    ai_manager.switch_provider(user_id, AIProvider.DEEPSEEK)
    await update.message.reply_text("🔄 Agora usando DeepSeek AI para processar suas mensagens!")

async def use_eden(update: Update, context: CallbackContext) -> None:
    """Switch to Eden AI."""
    user_id = update.effective_user.id
    ai_manager.switch_provider(user_id, AIProvider.EDEN)
    await update.message.reply_text("🔄 Agora usando Eden AI para processar suas mensagens!")

async def analyze_sentiment(update: Update, context: CallbackContext) -> None:
    """Enable sentiment analysis for the next message."""
    user_id = update.effective_user.id
    analyzing_sentiment[user_id] = True
    await update.message.reply_text("📊 Envie uma mensagem para análise de sentimento.")

async def list_databases(update: Update, context: CallbackContext) -> None:
    """Lista todos os bancos de dados acessíveis do Notion."""
    try:
        databases = await notion_client.list_databases()
        if not databases:
            await update.message.reply_text(
                "📚 Nenhum banco de dados encontrado no seu workspace Notion.\n\n"
                "Verifique se:\n"
                "1. O token de integração tem permissões corretas\n"
                "2. A integração foi adicionada aos bancos de dados\n"
                "3. O ID do banco de dados padrão está correto (se configurado)"
            )
            return

        response = "📚 Bancos de dados disponíveis no Notion:\n\n"
        for db in databases:
            response += f"📁 {db['title']}\n"
            response += f"ID: `{db['id']}`\n"
            if db.get('description'):
                response += f"📝 {db['description']}\n"
            response += "\n"

        await update.message.reply_text(response)
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Erro ao listar bancos de dados: {error_msg}")

        if "Token" in error_msg or "autenticação" in error_msg.lower():
            await update.message.reply_text(
                "❌ Erro de autenticação no Notion.\n\n"
                "Por favor, verifique:\n"
                "1. Se o token de integração está correto\n"
                "2. Se a integração tem permissões necessárias\n"
                "3. Se a integração não foi removida do workspace"
            )
        else:
            await update.message.reply_text(
                "❌ Erro ao listar bancos de dados do Notion.\n"
                "Por favor, verifique os logs para mais detalhes."
            )

async def use_dummy_mode(update: Update, context: CallbackContext) -> None:
    """Enable dummy mode."""
    user_id = update.effective_user.id
    ai_manager.enable_dummy_mode(user_id)
    providers = [AIManager.get_provider_name(p) for p in ai_manager.list_available_providers()]
    providers_text = "\n".join([f"- /use_{p.lower()} para usar {p}" for p in providers])

    await update.message.reply_text(
        f"🤖 Modo dummy ativado. Todas as IAs estão desativadas.\n\n"
        f"Provedores de IA disponíveis:\n{providers_text}"
    )

async def save_to_notion(update: Update, context: CallbackContext) -> None:
    """Salva a próxima mensagem no Notion."""
    if not context.args:
        await update.message.reply_text(
            "ℹ️ Por favor, forneça um título para a página.\n"
            "Exemplo: /save Minha Nota"
        )
        return

    user_id = update.effective_user.id
    title = " ".join(context.args)

    # Aguardando próxima mensagem
    context.user_data["waiting_for_notion_content"] = {
        "title": title,
        "command": "save"
    }

    await update.message.reply_text(
        f"📝 Título definido: '{title}'\n"
        "Agora envie o conteúdo que deseja salvar no Notion.\n"
        "Obs: O conteúdo será limitado a 2000 caracteres."
    )

async def search_notion(update: Update, context: CallbackContext) -> None:
    """Search in Notion."""
    if not context.args:
        await update.message.reply_text(
            "ℹ️ Por favor, forneça um termo para busca.\n"
            "Exemplo: /search reunião"
        )
        return

    query = " ".join(context.args)
    try:
        results = await notion_client.search_pages(query)
        if not results:
            await update.message.reply_text("🔍 Nenhum resultado encontrado.")
            return

        response = "🔍 Resultados encontrados:\n\n"
        for page in results:
            response += f"📄 {page['title']}\n"
            response += f"🔗 {page['url']}\n"
            response += f"⏱️ Última edição: {page['last_edited']}\n\n"

        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error searching Notion: {str(e)}")
        await update.message.reply_text(
            "❌ Erro ao buscar no Notion.\n"
            "Por favor, tente novamente mais tarde."
        )

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Processa todas as mensagens recebidas."""
    try:
        user_id = update.effective_user.id
        message_text = update.message.text

        # Verificar se estamos esperando conteúdo para o Notion
        if context.user_data.get("waiting_for_notion_content"):
            notion_data = context.user_data["waiting_for_notion_content"]

            if notion_data["command"] == "save":
                try:
                    result = await notion_client.create_page(
                        title=notion_data["title"],
                        content=message_text
                    )

                    # Se o conteúdo foi truncado, avisar o usuário
                    truncated_warning = ""
                    if len(message_text) > 2000:
                        truncated_warning = "\n⚠️ O conteúdo foi limitado a 2000 caracteres."

                    await update.message.reply_text(
                        "✅ Conteúdo salvo com sucesso no Notion!" +
                        truncated_warning + "\n\n"
                        f"📄 Título: {result['title']}\n"
                        f"🔗 Link: {result['url']}"
                    )
                except Exception as e:
                    error_msg = str(e)
                    logger.error(f"Erro ao salvar no Notion: {error_msg}")

                    if "Token" in error_msg:
                        await update.message.reply_text(
                            "❌ Erro de autenticação no Notion.\n"
                            "Por favor, verifique se o token de integração está correto."
                        )
                    elif "database" in error_msg.lower():
                        await update.message.reply_text(
                            "❌ Erro ao acessar o banco de dados do Notion.\n"
                            "Verifique se o ID do banco está correto e se você tem permissão de acesso."
                        )
                    else:
                        await update.message.reply_text(
                            "❌ Erro ao salvar no Notion.\n"
                            "Por favor, verifique se o conteúdo é válido e tente novamente."
                        )

                # Limpar o estado de espera
                del context.user_data["waiting_for_notion_content"]
                return

        # Verifica se está em modo dummy
        if ai_manager.is_dummy_mode(user_id):
            providers = [AIManager.get_provider_name(p) for p in ai_manager.list_available_providers()]
            providers_text = "\n".join([f"- /use_{p.lower()} para usar {p}" for p in providers])

            await update.message.reply_text(
                "😴 Sou incapaz de responder você. Modo dummy está ativado.\n\n"
                "Deseja ativar algum módulo de IA?\n"
                f"{providers_text}"
            )
            return

        # Verifica se a IA está ativada para o usuário
        if not ai_manager.is_enabled(user_id):
            await update.message.reply_text("🔇 IA está desativada. Use /toggle_ai para ativá-la.")
            return

        # Verifica se é para fazer análise de sentimento
        if analyzing_sentiment.get(user_id, False):
            analyzing_sentiment[user_id] = False  # Reset flag
            try:
                sentiment_results = await eden_client.analyze_sentiment(message_text)

                response = "📊 Análise de Sentimento:\n\n"

                if "amazon" in sentiment_results:
                    amazon = sentiment_results["amazon"]
                    response += "Amazon:\n"
                    response += f"- Sentimento: {amazon.get('sentiment', 'N/A')}\n"
                    response += f"- Confiança: {amazon.get('confidence', 0):.2f}%\n\n"

                if "google" in sentiment_results:
                    google = sentiment_results["google"]
                    response += "Google:\n"
                    response += f"- Sentimento: {google.get('sentiment', 'N/A')}\n"
                    response += f"- Confiança: {google.get('confidence', 0):.2f}%\n"

                await update.message.reply_text(response)
                return
            except Exception as e:
                logger.error(f"Error in sentiment analysis: {str(e)}")
                await update.message.reply_text("Erro ao analisar sentimento. Tente novamente.")
                return

        # Get AI response based on selected provider
        provider = ai_manager.get_active_provider(user_id)
        if provider == AIProvider.DEEPSEEK:
            response = await deepseek_client.get_response(message_text)
        else:  # AIProvider.EDEN
            response = await eden_client.get_response(message_text)

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
        application.add_handler(CommandHandler("toggle_ai", toggle_ai))
        application.add_handler(CommandHandler("use_deepseek", use_deepseek))
        application.add_handler(CommandHandler("use_eden", use_eden))
        application.add_handler(CommandHandler("use_dummy", use_dummy_mode))
        application.add_handler(CommandHandler("analyze_sentiment", analyze_sentiment))
        application.add_handler(CommandHandler("save", save_to_notion))
        application.add_handler(CommandHandler("search", search_notion))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Start the Bot
        logger.info("Starting bot...")
        application.run_polling()

    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")
        raise

if __name__ == '__main__':
    main()