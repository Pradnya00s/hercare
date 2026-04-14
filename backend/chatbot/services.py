import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")


def get_ai_response(user_message, language):

    prompt = f"""
    You are a professional Women Health AI Companion.
    Respond in {language}.
    Be medically responsible and supportive.
    """

    response = model.generate_content(prompt + "\nUser: " + user_message)

    return response.text
