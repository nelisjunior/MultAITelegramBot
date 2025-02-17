import aiohttp
import asyncio
import logging
from config import EDEN_AI_API_KEY
from langdetect import detect

logger = logging.getLogger(__name__)

class EdenAIClient:
    def __init__(self):
        self.api_key = EDEN_AI_API_KEY
        self.base_url = "https://api.edenai.run/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_response(self, message: str, context: dict = None) -> str:
        """
        Get AI response using Eden AI's Text Generation API
        """
        try:
            # Detect message language
            try:
                lang = detect(message)
                logger.info(f"Detected language: {lang}")
            except:
                lang = 'pt'  # Default to Portuguese if detection fails
                logger.warning("Language detection failed, defaulting to Portuguese")

            endpoint = f"{self.base_url}/text/generation"

            # Adjust system prompt based on language
            if lang == 'pt':
                system_prompt = """
                Você é um assistente AI que ajuda os usuários a gerenciar seu espaço de trabalho no Notion.
                Você pode ajudar a criar páginas, buscar conteúdo e organizar informações.
                Quando os usuários mencionarem bancos de dados ou páginas, tente entender a intenção
                deles e sugerir ações apropriadas.
                Responda sempre em português de forma natural e amigável.
                """
            else:
                system_prompt = """
                You are an AI assistant that helps users manage their Notion workspace.
                You can help create pages, search for content, and organize information.
                When users mention databases or pages, try to understand their intent
                and suggest appropriate actions.
                Always respond naturally and in a friendly manner.
                """

            prompt = f"{system_prompt}\n\nContext: {str(context)}\n\nUser: {message}" if context else f"{system_prompt}\n\nUser: {message}"

            payload = {
                "providers": "openai",
                "text": prompt,
                "temperature": 0.7,
                "max_tokens": 1000,
                "language": lang
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    endpoint,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    response.raise_for_status()
                    result = await response.json()

                    if result.get("openai") and result["openai"].get("generated_text"):
                        return result["openai"]["generated_text"]

                    error_msg = "Sem resposta válida dos provedores" if lang == 'pt' else "No valid response from providers"
                    raise Exception(error_msg)

        except asyncio.TimeoutError:
            error_msg = "Tempo limite excedido" if lang == 'pt' else "Request timed out"
            logger.error("Request to Eden AI timed out")
            raise TimeoutError(error_msg)

        except Exception as e:
            error_msg = "Erro ao processar requisição" if lang == 'pt' else "Error processing request"
            logger.error(f"Error calling Eden AI: {str(e)}")
            raise Exception(f"{error_msg}: {str(e)}")

    async def analyze_sentiment(self, text: str) -> dict:
        """
        Analyze sentiment of a text using Eden AI
        """
        try:
            # Detect text language
            try:
                lang = detect(text)
                logger.info(f"Detected language for sentiment analysis: {lang}")
            except:
                lang = 'pt'  # Default to Portuguese
                logger.warning("Language detection failed, defaulting to Portuguese")

            endpoint = f"{self.base_url}/text/sentiment_analysis"

            payload = {
                "providers": "amazon,google",
                "text": text,
                "language": lang
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    endpoint,
                    headers=self.headers,
                    json=payload
                ) as response:
                    response.raise_for_status()
                    result = await response.json()

                    return {
                        "amazon": result.get("amazon", {}),
                        "google": result.get("google", {})
                    }

        except Exception as e:
            error_msg = "Erro na análise de sentimento" if lang == 'pt' else "Error in sentiment analysis"
            logger.error(f"Error in sentiment analysis: {str(e)}")
            raise Exception(f"{error_msg}: {str(e)}")