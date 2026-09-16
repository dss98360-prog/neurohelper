from pathlib import Path
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import (
    APIConnectionError,
    APIError,
    APIStatusError,
    APITimeoutError,
    OpenAI,
    RateLimitError,
)
from pydantic import BaseModel

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)

VSEGPT_BASE_URL = "https://api.vsegpt.ru/v1"
# Подтверждено через GET https://api.vsegpt.ru/v1/models
VSEGPT_MODEL = "openai/gpt-4.1-nano"


SYSTEM_PROMPT = """Ты — «Нейропомощник», универсальный персональный AI-ассистент.

Помогай пользователю решать повседневные, учебные и рабочие задачи.

Общие правила:
- отвечай на русском языке, если пользователь не попросил другой язык;
- сначала давай полезный результат, затем при необходимости пояснение;
- пиши понятно, конкретно и структурированно;
- не добавляй лишнюю теорию;
- если данных недостаточно для точного ответа, сообщи об этом;
- не выдумывай факты;
- сохраняй дружелюбный и профессиональный стиль.
"""

MODE_PROMPTS = {
    "free": "Отвечай на запрос пользователя в наиболее подходящем формате.",
    "plan": "Составь понятный пошаговый план действий. Используй нумерованные этапы.",
    "checklist": "Составь практический чек-лист. Используй короткие пункты с отметками.",
    "text": "Напиши готовый текст по запросу пользователя. Сразу дай вариант, который можно использовать.",
    "ideas": "Предложи несколько конкретных и разнообразных идей. Кратко поясни каждую.",
    "explain": "Объясни тему простыми словами. При необходимости используй понятный пример.",
}

app = FastAPI(title="neurohelper")


class AskRequest(BaseModel):
    message: str
    mode: str = "free"


def get_vsegpt_api_key() -> str | None:
    key = os.getenv("VSEGPT_API_KEY")
    if key is None:
        return None
    key = key.strip()
    if not key or key == "your_vsegpt_api_key_here":
        return None
    return key


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "neurohelper",
    }


@app.post("/api/ask")
def ask(payload: AskRequest):
    message = (payload.message or "").strip()
    if not message:
        raise HTTPException(
            status_code=400,
            detail="Сообщение не должно быть пустым.",
        )

    api_key = get_vsegpt_api_key()
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Ключ VseGPT не найден. Создайте файл .env в корне проекта и добавьте VSEGPT_API_KEY.",
        )

    client = OpenAI(api_key=api_key, base_url=VSEGPT_BASE_URL)
    mode = (payload.mode or "free").strip().lower()
    mode_prompt = MODE_PROMPTS.get(mode, MODE_PROMPTS["free"])
    try:
        response = client.chat.completions.create(
            model=VSEGPT_MODEL,
            messages=[
                {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nРежим ответа:\n{mode_prompt}"},
                {"role": "user", "content": message},
            ],
        )
        answer = (response.choices[0].message.content or "").strip()
        if not answer:
            raise HTTPException(
                status_code=502,
                detail="Модель вернула пустой ответ. Попробуйте ещё раз.",
            )
        return {"answer": answer}
    except HTTPException:
        raise
    except APITimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Сервис VseGPT слишком долго отвечает. Попробуйте позже.",
        )
    except APIConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Не удалось подключиться к сервису VseGPT. Проверьте интернет и попробуйте позже.",
        )
    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="Слишком много запросов. Подождите немного и попробуйте снова.",
        )
    except APIStatusError as exc:
        if exc.status_code in (401, 403):
            raise HTTPException(
                status_code=502,
                detail="VseGPT отклонил запрос. Проверьте ключ VSEGPT_API_KEY в файле .env.",
            )
        if exc.status_code in (502, 503, 504):
            raise HTTPException(
                status_code=503,
                detail="Сервис VseGPT временно недоступен. Попробуйте позже.",
            )
        raise HTTPException(
            status_code=502,
            detail="Не удалось получить ответ от VseGPT. Попробуйте ещё раз.",
        )
    except APIError:
        raise HTTPException(
            status_code=502,
            detail="Произошла ошибка при обращении к VseGPT. Попробуйте ещё раз.",
        )
