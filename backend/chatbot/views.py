import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ChatMessage


CRISIS_KEYWORDS = [
    "kill myself",
    "suicide",
    "end my life",
    "self harm",
    "want to die",
    "can't live anymore"
]


@csrf_exempt
def chat_with_ai(request):

    # Allow only POST request
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        user_message = data.get("message", "")

        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)

        user_message_lower = user_message.lower()

        # 🚨 Crisis Detection
        if any(keyword in user_message_lower for keyword in CRISIS_KEYWORDS):

            crisis_reply = (
                "I'm really sorry you're feeling this way. "
                "You are not alone 💙\n\n"
                "If you're in immediate danger, please call your local emergency number.\n"
                "In India, you can contact the Kiran Mental Health Helpline: 1800-599-0019.\n\n"
                "Would you like to talk more about what you're feeling?"
            )

            # Save to database
            ChatMessage.objects.create(
                user_message=user_message,
                ai_response=crisis_reply
            )

            return JsonResponse({"response": crisis_reply})

        # 🤖 Normal AI response from Ollama
        ollama_response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a calm, empathetic mental health assistant. "
                            "Respond gently and supportively to help users feel heard and supported."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "stream": False
            }
        )

        ollama_data = ollama_response.json()

        ai_reply = ollama_data["message"]["content"]

        # 💾 Save chat to database
        ChatMessage.objects.create(
            user_message=user_message,
            ai_response=ai_reply
        )

        return JsonResponse({"response": ai_reply})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)