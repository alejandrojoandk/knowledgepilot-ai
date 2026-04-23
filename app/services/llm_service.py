
import time

from groq import Groq

from app.core.config import settings
from app.core.prompts import SYSTEM_PROMPT


class LLMService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    def chat(self, message: str, model_name: str | None = None):
        selected_model = model_name or settings.model_name

        start = time.time()

        response = self.client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message},
            ],
            temperature=0.3,
        )

        latency_ms = int((time.time() - start) * 1000)

        reply = response.choices[0].message.content

        return {
            "reply": reply,
            "latency_ms": latency_ms,
            "model": selected_model,
        }


llm_service = LLMService()