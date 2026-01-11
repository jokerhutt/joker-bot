from google import genai
import os
from typing import Optional

_client: Optional[genai.Client] = None
_aclient = None


def get_genai_aclient():
    global _client, _aclient

    if _aclient is not None:
        return _aclient

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set")

    _client = genai.Client(api_key=api_key)
    _aclient = _client.aio
    return _aclient


async def generate_ai_response(full_prompt: str):
    aclient = get_genai_aclient()
    resp = await aclient.models.generate_content(
        model="gemini-2.5-flash-lite", contents=full_prompt
    )

    return resp
