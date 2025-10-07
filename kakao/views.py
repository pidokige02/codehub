# views.py
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render

@csrf_exempt  # 개발 중에는 편의상 사용, 배포 전에는 주의
def book_search(request):
    query = request.GET.get('query', '')
    page = int(request.GET.get("page", 1))   # 기본 1페이지
    size = int(request.GET.get("size", 10))  # 기본 10개

    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)

    url = "https://dapi.kakao.com/v3/search/book"
    headers = {
        "Authorization": f"{settings.KAKAO_API_KEY}"  # 실제 키로 교체
    }
    params = {
        "target": "title",
        "query": query,
        "page": page,
        "size": size,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
# url 에 header 와 param 을 넘기는 방법이 나와 있고, 결과를 json 방식으로 client 에  넘기고 있다.

def kakao_map(request):
    """
    Kakao JavaScript SDK를 이용한 지도 페이지
    (AppKey는 서버에서 안전하게 주입)
    """
    context = {
        "kakao_key": settings.KAKAO_JS_KEY,
    }
    return render(request, "kakao/map.html", context)
