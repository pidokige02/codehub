import pandas as pd
import re
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import BibleVersion, BibleVerse
from .forms import ExcelUploadForm


def parse_reference(reference):
    """
    'Genesis 1:1' 형태의 문자열을 분리하여 book, chapter, verse를 추출하는 함수.
    """
    match = re.match(r'([\w\s]+)\s(\d+):(\d+)', str(reference))
    if match:
        book = match.group(1).strip()  # 'Genesis'
        chapter = int(match.group(2))  # 1
        verse = int(match.group(3))  # 1
        return book, chapter, verse
    return None, None, None

@staff_member_required
def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.save()
            file_path = excel_file.file.path  # 업로드된 파일 경로

            # Excel 데이터 읽기
            df = pd.read_excel(file_path, header=None)  # 헤더 없음 가정

            # 1~2번째 행: 성경 번역본 정보 저장
            version_code = df.iloc[0, 1]  # 예: "ERV"
            version_name = df.iloc[1, 1]  # 예: "English Revised Version"

            # 번역본이 이미 존재하는지 확인 후 저장
            version, created = BibleVersion.objects.get_or_create(
                code=version_code,
                defaults={'name': version_name}
            )

            # 3번째 행부터 성경 구절 저장
            first_book, first_chapter = None, None  # 첫 번째 저장된 구절 정보

            for i in range(2, len(df)):  # 0-based index → 2부터 시작
                reference, text = df.iloc[i, 0], df.iloc[i, 1]
                book, chapter, verse = parse_reference(reference)

                if book and chapter and verse:
                    BibleVerse.objects.create(
                        version=version,
                        book=book,
                        chapter=chapter,
                        verse=verse,
                        text=text
                    )
                    if first_book is None and first_chapter is None:
                        first_book, first_chapter = book, chapter  # 첫 구절 저장

            # 저장된 첫 번째 책과 장(chapter)으로 리디렉트
            if first_book and first_chapter:
                return redirect(reverse('bibleview:bible_list', args=[first_book, first_chapter]))

    else:
        form = ExcelUploadForm()

    return render(request, 'bibleview/upload_excel.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from bibleview.models import BibleVersion, BibleVerse

def bible_list(request, book, chapter):
    # GET 요청에서 선택한 성경 버전 가져오기 (기본값: 첫 번째 버전)
    version_code = request.GET.get("version_code", None)

    # 성경 버전이 유효한지 확인하고, 없으면 기본값 설정
    if version_code:
        version = BibleVersion.objects.filter(code=version_code).first()
    else:
        version = BibleVersion.objects.first()  # 기본값: 첫 번째 성경 버전

    if not version:  # 데이터베이스에 아무 버전도 없을 경우
        return render(request, "bibleview/error.html", {"error": "성경 버전 데이터가 없습니다."})

    version_code = version.code  # 유효한 version_code 사용

    # 해당 책의 모든 장 번호 가져오기
    total_chapters = list(BibleVerse.objects.filter(version=version, book=book)
                          .values_list("chapter", flat=True)
                          .distinct()
                          .order_by("chapter"))

    if not total_chapters:  # 해당 책이 존재하지 않을 경우
        return render(request, "bibleview/error.html", {"error": f"{book}에 대한 데이터가 없습니다."})

    # `chapter`가 정수인지 확인하고, 존재하는 장인지 검증
    try:
        chapter = int(chapter)
        if chapter not in total_chapters:
            return render(request, "bibleview/error.html", {"error": f"{book}에는 {chapter}장이 존재하지 않습니다."})
    except ValueError:  # chapter가 정수가 아닐 경우
        return render(request, "bibleview/error.html", {"error": "잘못된 장 번호입니다."})

    # 선택한 버전, 책, 장에 해당하는 구절 가져오기
    verses = BibleVerse.objects.filter(version=version, book=book, chapter=chapter).order_by("verse")

    # 모든 책 목록 가져오기
    books = list(BibleVerse.objects.filter(version=version).values_list("book", flat=True).distinct())

    # 페이지네이션을 위한 챕터 목록 만들기
    def get_chapter_pagination(chapters, current_chapter):
        max_display = 10  # 한 번에 표시할 최대 개수

        if len(chapters) <= max_display:  # 전체 개수가 적으면 그냥 표시
            return chapters

        result = []
        first, last = chapters[0], chapters[-1]

        # 항상 첫 번째 챕터 추가
        result.append(first)

        if current_chapter > 6:
            result.append("...")  # 앞부분 축약

        # 현재 장을 중심으로 몇 개만 보여주기
        for num in range(current_chapter - 4, current_chapter + 5):
            if first < num < last:
                result.append(num)

        if current_chapter < last - 5:
            result.append("...")  # 뒷부분 축약

        # 항상 마지막 챕터 추가
        result.append(last)
        return result

    paginated_chapters = get_chapter_pagination(total_chapters, chapter)

    return render(request, "bibleview/bible_list.html", {
        "book": book,
        "chapter": chapter,
        "verses": verses,
        "total_chapters": paginated_chapters,  # UI에서 축약된 챕터 리스트 사용
        "version_code": version_code,
        "versions": BibleVersion.objects.all(),  # 템플릿에서 버전 선택 가능하도록 전달
        "books": books,  # 책 목록 추가
    })

