from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'googleapp'  # URL 네임스페이스 설정

urlpatterns = [
    path("Gemini/", views.gemini_page, name="gemini_page"),
]
