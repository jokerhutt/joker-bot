from google import genai
import os

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
aclient = client.aio


async def generate_ai_response(full_prompt: str):

    resp = await aclient.models.generate_content(
        model="gemini-2.5-flash-lite", contents=full_prompt
    )

    return resp
