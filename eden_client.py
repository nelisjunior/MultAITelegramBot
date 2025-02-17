import aiohttp
import asyncio
import logging
from config import EDEN_AI_API_KEY

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
            endpoint = f"{self.base_url}/text/generation"

            # Prepare system context if provided
            system_prompt = """
            You are an AI assistant that helps users manage their Notion workspace.
            You can help create pages, search for content, and organize information.
            When users mention databases or pages, try to understand their intent
            and suggest appropriate actions.
            """

            prompt = f"{system_prompt}\n\nContext: {str(context)}\n\nUser: {message}" if context else f"{system_prompt}\n\nUser: {message}"

            payload = {
                "providers": "openai",  # Você pode adicionar outros provedores como "anthropic", "cohere"
                "text": prompt,
                "temperature": 0.7,
                "max_tokens": 1000
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

                    # Eden AI retorna respostas de diferentes provedores
                    # Vamos usar o OpenAI como padrão
                    if result.get("openai") and result["openai"].get("generated_text"):
                        return result["openai"]["generated_text"]

                    raise Exception("No valid response from Eden AI providers")

        except asyncio.TimeoutError:
            logger.error("Request to Eden AI timed out")
            raise TimeoutError("The request to Eden AI timed out")

        except Exception as e:
            logger.error(f"Error calling Eden AI: {str(e)}")
            raise Exception(f"Error processing request: {str(e)}")

    async def analyze_sentiment(self, text: str) -> dict:
        """
        Analyze sentiment of a text using Eden AI
        """
        try:
            endpoint = f"{self.base_url}/text/sentiment_analysis"

            payload = {
                "providers": "amazon,google",
                "text": text,
                "language": "pt-BR"
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
            logger.error(f"Error in sentiment analysis: {str(e)}")
            raise Exception(f"Error analyzing sentiment: {str(e)}")