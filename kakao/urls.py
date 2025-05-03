# urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'kakao'  # URL 네임스페이스 설정

urlpatterns = [
    path('api/book_search/', views.book_search, name='book_search'),
    path('search/book/', TemplateView.as_view(template_name="kakao/book_search.html")),
]