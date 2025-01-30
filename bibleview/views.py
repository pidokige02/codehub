import pandas as pd
import re
from django.shortcuts import render, redirect
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

            return redirect('bibleview:bible_list')

    else:
        form = ExcelUploadForm()

    return render(request, 'bibleview/upload_excel.html', {'form': form})


def bible_list(request, book, chapter):
    # 해당 책과 장의 모든 구절 가져오기
    verses = BibleVerse.objects.filter(book=book, chapter=chapter).order_by("verse")

    # 해당 책의 모든 장 번호 가져오기
    total_chapters = BibleVerse.objects.filter(book=book).values_list("chapter", flat=True).distinct().order_by("chapter")

    # 성경 버전 가져오기
    version_code = verses.first().version.code if verses.exists() else "개역한글"

    # 페이지네이션을 위한 챕터 목록 만들기
    def get_chapter_pagination(chapters, current_chapter):
        chapters = list(chapters)  # QuerySet을 리스트로 변환
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

    # 해당 책과 장의 모든 구절 가져오기
    verses = BibleVerse.objects.filter(book=book, chapter=chapter).order_by("verse")

    return render(request,"bibleview/bible_list.html", {
        "book": book,
        "chapter": chapter,
        "verses": verses,
        "total_chapters": paginated_chapters,  # UI에서 축약된 챕터 리스트 사용
        "version_code": version_code
    })