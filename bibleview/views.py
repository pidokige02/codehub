from django.shortcuts import render

def index(request):
    """BibleView 홈 화면"""
    return render(request, 'bibleview/index.html')

def search(request):
    """성경 검색 기능"""
    query = request.GET.get('q', '')
    return render(request, 'bibleview/search.html', {'query': query})

def verse_detail(request, book_id, chapter, verse):
    """특정 성경 구절 조회"""
    return render(request, 'bibleview/verse_detail.html', {
        'book_id': book_id,
        'chapter': chapter,
        'verse': verse
    })
