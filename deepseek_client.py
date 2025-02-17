import aiohttp
import asyncio
import logging
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
from langdetect import detect

logger = logging.getLogger(__name__)

class DeepSeekClient:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.api_url = DEEPSEEK_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_response(self, message: str, context: dict = None) -> str:
        """
        Get response from DeepSeek API asynchronously
        """
        try:
            # Detect message language
            try:
                lang = detect(message)
                logger.info(f"Detected language: {lang}")
            except:
                lang = 'pt'  # Default to Portuguese if detection fails
                logger.warning("Language detection failed, defaulting to Portuguese")

            # Simple system prompt focused on task
            system_prompt = "Responda em português de forma natural" if lang == 'pt' else "Respond naturally in English"

            messages = [
                {"role": "system", "content": system_prompt},
            ]

            if context:
                context_msg = "Contexto: " if lang == 'pt' else "Context: "
                messages.append({
                    "role": "system",
                    "content": f"{context_msg}{str(context)}"
                })

            messages.append({"role": "user", "content": message})

            payload = {
                "model": "deepseek-chat",
                "messages": messages,
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

                    return result['choices'][0]['message']['content'].strip()

        except asyncio.TimeoutError:
            error_msg = "Tempo limite excedido" if lang == 'pt' else "Request timed out"
            logger.error("Request to DeepSeek API timed out")
            raise TimeoutError(error_msg)

        except Exception as e:
            error_msg = "Erro ao processar requisição" if lang == 'pt' else "Error processing request"
            logger.error(f"Error calling DeepSeek API: {str(e)}")
            raise Exception(f"{error_msg}: {str(e)}")