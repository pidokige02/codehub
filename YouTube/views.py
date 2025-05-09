import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@csrf_exempt  # 개발 중에는 허용, 배포 시는 보안 설정 강화 필요
def YouTube_search(request):
    query = request.GET.get('query', '')
    page_token = request.GET.get('pageToken', '')

    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)

    YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY  # settings.py에 저장된 키 사용

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "maxResults": 25,
        "order": "relevance",
        "type": "video"
    }

    if page_token:
        params["pageToken"] = page_token

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
