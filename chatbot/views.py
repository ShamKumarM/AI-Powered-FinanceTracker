from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatBot
import google.generativeai as genai

# ✅ Configure your Gemini API key here
genai.configure(api_key="AIzaSyBEgbo2MIsVWSu4vbRaOwipmU7bBmZiY08")  # 🔐 Replace with actual key securely in production!

@login_required
def chatbot_interface(request):
    # ✅ Display last 10 messages for the logged-in user
    chat_history = ChatBot.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'chatbot/chatbot_interface.html', {'chat_history': chat_history})

@login_required
def chatbot_response(request):
    if request.method == "POST":
        # ✅ Clear chat history if requested
        if 'clear_chat' in request.POST:
            ChatBot.objects.filter(user=request.user).delete()
            return redirect('chatbot_interface')

        # ✅ Process user input
        user_input = request.POST.get("user_input")
        if not user_input:
            return JsonResponse({"error": "No input provided."}, status=400)

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_input)
            output = response.text
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        # ✅ Save to database
        ChatBot.objects.create(
            user=request.user,
            text_input=user_input,
            gemini_output=output
        )

        return redirect('chatbot_interface')

    return JsonResponse({"error": "Invalid request method"}, status=400)
