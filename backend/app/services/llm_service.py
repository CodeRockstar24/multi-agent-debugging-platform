import time
from google import genai
from app.core.config import settings


def get_gemini_client():
    return genai.Client(api_key=settings.gemini_api_key)


def generate_gemini_text(prompt: str, max_retries: int = 2) -> str:
    if not settings.gemini_api_key:
        return "Gemini API key is missing."

    client = get_gemini_client()
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text or "No response generated."
        except Exception as error:
            last_error = error
            if attempt < max_retries:
                time.sleep(1.5 * (attempt + 1))

    return f"LLM generation failed after retries: {last_error}"


def generate_embedding(text: str) -> list[float]:
    if not settings.gemini_api_key:
        return []

    try:
        client = get_gemini_client()
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
        )

        embeddings = getattr(response, "embeddings", None)
        if not embeddings:
            return []

        first = embeddings[0]
        values = getattr(first, "values", None)
        return values or []
    except Exception:
        return []
