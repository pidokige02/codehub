# views.py
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt  # 개발 중에는 편의상 사용, 배포 전에는 주의
def book_search(request):
    query = request.GET.get('query', '')

    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)

    url = "https://dapi.kakao.com/v3/search/book"
    headers = {
        "Authorization": f"{settings.KAKAO_API_KEY}"  # 실제 키로 교체
    }
    params = {
        "target": "title",
        "query": query
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
# url 에 header 와 param 을 넘기는 방법이 나와 있고, 결과를 json 방식으로 client 에  넘기고 있다.
