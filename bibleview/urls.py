from django.urls import path
from .views import upload_excel, bible_list, bible_list_api, upload_excel_api, upload_async_excel

app_name = 'bibleview'  # URL 네임스페이스 설정

urlpatterns = [
    path('upload/', upload_excel, name='upload_excel'),
    path('upload-api/', upload_excel_api, name='upload_excel_api'),
    path('upload-async/', upload_async_excel, name='upload_async_excel'),
    path("view/<str:book>/<int:chapter>/", bible_list, name="bible_list"),
    path('view-api/<str:book>/<int:chapter>/', bible_list_api, name='bible_list_api'),
]
