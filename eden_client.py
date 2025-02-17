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

    async def get_response(self, message: str) -> str:
        """
        Get AI response using Eden AI's Text Generation API
        """
        try:
            endpoint = f"{self.base_url}/text/generation"

            payload = {
                "providers": "openai",
                "text": message,
                "temperature": 0.3,
                "max_tokens": 150
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
                        return result["openai"]["generated_text"].strip()

                    raise Exception("No valid response from providers")

        except asyncio.TimeoutError:
            logger.error("Request to Eden AI timed out")
            raise TimeoutError("Timeout error")

        except Exception as e:
            logger.error(f"Error calling Eden AI: {str(e)}")
            raise Exception(f"Error: {str(e)}")

    async def analyze_sentiment(self, text: str) -> dict:
        """
        Analyze sentiment of a text using Eden AI
        """
        try:
            endpoint = f"{self.base_url}/text/sentiment_analysis"

            payload = {
                "providers": "amazon,google",
                "text": text
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
            raise Exception(f"Error in sentiment analysis: {str(e)}")