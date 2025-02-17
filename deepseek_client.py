import aiohttp
import asyncio
import logging
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL

logger = logging.getLogger(__name__)

class DeepSeekClient:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.api_url = DEEPSEEK_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_response(self, message: str) -> str:
        """
        Get response from DeepSeek API asynchronously
        """
        try:
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": message}],
                "temperature": 0.7,
                "max_tokens": 1000
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    response.raise_for_status()
                    result = await response.json()

                    return result['choices'][0]['message']['content']

        except asyncio.TimeoutError:
            logger.error("Request to DeepSeek API timed out")
            raise TimeoutError("The request to DeepSeek API timed out")

        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {str(e)}")
            raise Exception(f"Error processing request: {str(e)}")