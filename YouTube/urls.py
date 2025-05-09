# urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'YouTube'  # URL 네임스페이스 설정

urlpatterns = [
    path('api/search/', views.YouTube_search, name='search'),
    path('search/', TemplateView.as_view(template_name="YouTube/youtube_search.html"))
]