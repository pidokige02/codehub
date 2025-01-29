from django.urls import path
from . import views

app_name = 'bibleview'  # URL 네임스페이스 설정

urlpatterns = [
    path('', views.index, name='index'),  # 기본 페이지
    path('search/', views.search, name='search'),  # 성경 검색 기능
    path('verse/<int:book_id>/<int:chapter>/<int:verse>/', views.verse_detail, name='verse_detail'),  # 특정 구절 조회
]
