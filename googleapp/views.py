import os
from django.shortcuts import render
import google.generativeai as genai
from django.conf import settings


genai.configure(api_key=settings.GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-pro")


def gemini_page(request):
    context = {}
    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        if question:
            try:
                response = model.generate_content(question)
                context["history"] = [{
                    "question": question,
                    "answer": response.text
                }]
            except Exception as e:
                context["error"] = str(e)
        else:
            context["error"] = "질문을 입력해주세요."

    return render(request, "googleapp/gemini.html", context)