from django.shortcuts import render

# for local application only
def home(request):
    # 전달할 컨텍스트 데이터 (필요한 경우)
    context = {
        "title": "Default Layout",
        "message": "Welcome to the Default Layout Page",
    }
    return render(request, "home/index.html", context)


# for local application only
def about(request):
    return render(request, 'home/about.html')  # about.html 템플릿을 렌더링
