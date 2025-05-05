from django.urls import path
from .views import upload_excel, bible_list, bible_api

app_name = 'bibleview'  # URL 네임스페이스 설정

urlpatterns = [
    path('upload/', upload_excel, name='upload_excel'),
    path("view/<str:book>/<int:chapter>/", bible_list, name="bible_list"),
    path('apiview/<str:book>/<int:chapter>/', bible_api, name='bible_api'),
]
